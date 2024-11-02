import os
import asyncio
import aiohttp
from ..config import BASE_URL
from ..utils.file_manager import create_folder_for_prompt

async def generate_audio_by_prompt_async(prompt, session):
    """
    Async version of generate_audio_by_prompt
    """
    payload = {
        "prompt": prompt,
        "make_instrumental": True,
        "wait_audio": False
    }
    url = f"{BASE_URL}/api/generate"
    try:
        async with session.post(url, json=payload) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        print(f"Error generating audio for prompt '{prompt}': {e}")
        return None

async def get_audio_information_async(audio_ids, session):
    """
    Async version of get_audio_information
    """
    url = f"{BASE_URL}/api/get?ids={audio_ids}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        print(f"Error retrieving audio information for IDs '{audio_ids}': {e}")
        return None

async def download_audio_file_async(audio_url, file_path, session, retries=3):
    """
    Async version of download_audio_file
    """
    for attempt in range(retries):
        try:
            async with session.get(audio_url) as response:
                response.raise_for_status()
                with open(file_path, 'wb') as audio_file:
                    audio_file.write(await response.read())
            print(f"Downloaded: {file_path}")
            return True
        except Exception as e:
            print(f"Attempt {attempt+1}/{retries} failed to download {file_path}: {e}")
            await asyncio.sleep(2)
    print(f"Failed to download {file_path} after {retries} attempts.")
    return False

async def generate_all_songs_async(titles_and_prompts, music_folder, concurrent_limit=3):
    """
    Generates multiple songs concurrently with a limit on simultaneous generations
    """
    all_songs = []
    semaphore = asyncio.Semaphore(concurrent_limit)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for title, prompt in titles_and_prompts:
            task = asyncio.create_task(generate_single_song(
                title, prompt, music_folder, session, semaphore
            ))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                print(f"Error generating song: {result}")
            elif result:
                # Flatten the list of variations into the main song list
                all_songs.extend(result)
    
    return all_songs

async def generate_single_song(title, prompt, music_folder, session, semaphore):
    """
    Generates a single song with the given prompt using Suno AI
    """
    async with semaphore:
        try:
            prompt_folder = create_folder_for_prompt(prompt, music_folder)
            
            # Generate the audio
            response = await generate_audio_by_prompt_async(prompt, session)
            if not response:
                return None
            
            # The response contains a list of two variations
            if not isinstance(response, list) or len(response) < 2:
                print(f"Unexpected response format for prompt: {prompt}")
                return None
            
            ids = f"{response[0]['id']},{response[1]['id']}"
            print(f"Song IDs: {ids}")
            
            # Wait and get the audio information
            for _ in range(30):  # Maximum 5 minutes wait (10 seconds * 30)
                audio_info = await get_audio_information_async(ids, session)
                if audio_info and audio_info[0]["status"] == 'streaming' and audio_info[1]["status"] == 'streaming':
                    download_tasks = []
                    for i, variant in enumerate(['A', 'B']):
                        audio_url = audio_info[i]["audio_url"]
                        file_path = os.path.join(prompt_folder, f"{audio_info[i]['id']}.mp3")
                        download_tasks.append(download_audio_file_async(audio_url, file_path, session))
                    
                    results = await asyncio.gather(*download_tasks)
                    if all(results):
                        song_info = []
                        for i, variant in enumerate(['A', 'B']):
                            song_info.append({
                                'title': f"{title} (Variation {variant})",
                                'file_path': os.path.join(prompt_folder, f"{audio_info[i]['id']}.mp3"),
                                'id': audio_info[i]['id']
                            })
                        return song_info
                    break
                await asyncio.sleep(5)
            
            print(f"Timeout waiting for audio generation: {title}")
            return None
            
        except Exception as e:
            print(f"Error generating song '{title}': {e}")
            return None