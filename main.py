import os
import asyncio
from src.utils.file_manager import create_run_folders
from src.utils.prompt_generator import get_prompts_from_gpt
from src.audio.generator import generate_all_songs_async
from src.audio.processor import concatenate_audio_files
from src.image.generator import generate_background_image
from src.video.creator import create_video_with_image
from src.youtube.uploader import generate_video_metadata, upload_to_youtube

async def main():
    # Create folder structure for this run
    folders = create_run_folders()
    
    # Get prompts and titles
    titles_and_prompts = get_prompts_from_gpt()
    print(f"Titles and Prompts: {titles_and_prompts}")
    
    # Generate individual songs and track their information
    all_songs = await generate_all_songs_async(titles_and_prompts, folders['music_segments'], concurrent_limit=3)
    
    # Combine audio files and get timestamps
    combined_audio_path, timestamps = concatenate_audio_files(all_songs, folders['music'])
    
    # Generate and save background image
    image_path = generate_background_image(titles_and_prompts, folders['photos'])
    
    # Create and save video
    output_video_path = os.path.join(folders['videos'], "playlist_video.mp4")
    create_video_with_image(combined_audio_path, image_path, output_video_path)
    
    # Generate metadata and upload to YouTube
    print("\nGenerating video metadata...")
    title, description = generate_video_metadata(timestamps)
    
    print("\nUploading to YouTube...")
    video_id = upload_to_youtube(output_video_path, title, description)
    
    if video_id:
        print(f"\nVideo uploaded successfully! ID: {video_id}")
    else:
        print("\nVideo upload failed.")
    
    print(f"\nRun completed! All files are stored in: {os.path.dirname(folders['music'])}")

if __name__ == "__main__":
    asyncio.run(main())