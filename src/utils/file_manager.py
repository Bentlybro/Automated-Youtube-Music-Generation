import os
import time
import hashlib
import re

def create_run_folders():
    """
    Creates a structured folder hierarchy for the current run using timestamp
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_folder = os.path.join("Output", timestamp)
    
    folders = {
        'music': os.path.join(base_folder, 'music'),
        'photos': os.path.join(base_folder, 'photos'),
        'videos': os.path.join(base_folder, 'videos'),
        'music_segments': os.path.join(base_folder, 'music', 'segments')
    }
    
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
        
    return folders

def create_folder_for_prompt(prompt, base_folder):
    """
    Creates a folder for individual prompt within the music segments folder
    """
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
    sanitized_prompt = re.sub(r'[<>:"/\\|?*]', '', prompt)[:30]
    prompt_folder = os.path.join(base_folder, f"{sanitized_prompt}_{prompt_hash}")
    
    os.makedirs(prompt_folder, exist_ok=True)
    return prompt_folder