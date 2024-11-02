import random
from pydub import AudioSegment
import os

def concatenate_audio_files(all_songs, music_folder):
    """
    Combines multiple audio files into a single playlist
    """
    combined_audio = AudioSegment.empty()
    current_position = 0
    timestamps = []
    
    random.shuffle(all_songs)
    
    print("\nAdding songs in random order:")
    for i, song in enumerate(all_songs, 1):
        try:
            audio = AudioSegment.from_mp3(song['file_path'])
            
            duration_seconds = len(audio) / 1000
            if duration_seconds < 60:
                print(f"Skipping {song['title']} - Duration too short ({duration_seconds:.1f} seconds)")
                continue
            
            combined_audio += audio
            
            total_seconds = current_position / 1000
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            
            timestamp = f"{hours}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"
            
            timestamps.append({
                'title': song['title'],
                'timestamp': timestamp
            })
            
            current_position += len(audio)
            print(f"{i}. Added {song['title']} - Position: {timestamp} - Duration: {duration_seconds:.1f}s")
        except Exception as e:
            print(f"Error loading file {song['file_path']}: {e}")

    output_audio_path = os.path.join(music_folder, "combined_playlist.mp3")
    combined_audio.export(output_audio_path, format="mp3")
    
    print(f"\nCombined audio saved as {output_audio_path}")
    print(f"Final playlist duration: {len(combined_audio)/1000/60:.2f} minutes")
    print(f"Total songs added: {len(timestamps)}")
    return output_audio_path, timestamps