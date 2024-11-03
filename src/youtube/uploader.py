import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from ..config import (
    YOUTUBE_SCOPES,
    YOUTUBE_API_NAME,
    YOUTUBE_API_VERSION,
    CLIENT_SECRETS_FILE,
    TOKEN_FILE,
    anthropic_client
)

def generate_video_metadata(timestamps):
    """
    Generates YouTube video title and description with timestamps
    """
    prompt = """
    Create a YouTube video title and description for a lofi jazz music mix. The video contains multiple original AI-generated lofi jazz songs.

    Requirements:
    1. Title should be catchy and SEO-friendly (max 100 characters)
    2. Description should include:
       - Brief introduction about the mix
       - Mention that all music is AI-generated
       - Relevant hashtags
       - A timestamp placeholder [TIMESTAMPS]

    Format your response as:
    TITLE: [your title here]
    DESCRIPTION:
    [your description here]
    """
    
    response = anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    content = response.content[0].text
    title_line = [line for line in content.splitlines() if line.startswith("TITLE:")][0]
    title = title_line.replace("TITLE:", "").strip()
    
    description_start = content.find("DESCRIPTION:") + len("DESCRIPTION:")
    description = content[description_start:].strip()
    
    timestamp_text = "\nTIMESTAMPS:\n"
    for ts in timestamps:
        timestamp_text += f"{ts['timestamp']} - {ts['title']}\n"
    
    description = description.replace("[TIMESTAMPS]", timestamp_text)
    
    # Add GitHub link to the end of the description
    github_link = "\n\n🔗 Check out the code behind this project: https://github.com/Bentlybro/Automated-Youtube-Music-Generation"
    description += github_link
    
    return title, description

def upload_to_youtube(video_path, title, description):
    """
    Uploads video to YouTube as private
    """
    credentials = None
    
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, YOUTUBE_SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
                credentials = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            credentials = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())
    
    youtube = build(YOUTUBE_API_NAME, YOUTUBE_API_VERSION, credentials=credentials)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['lofi', 'jazz', 'music', 'study music', 'AI generated'],
            'categoryId': '10'  # Music category
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        }
    }
    
    try:
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True
        )
        
        upload_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = upload_request.execute()
        print(f"Upload successful! Video ID: {response['id']}")
        print(f"Video URL: https://youtube.com/watch?v={response['id']}")
        return response['id']
        
    except Exception as e:
        print(f"An error occurred during upload: {e}")
        return None