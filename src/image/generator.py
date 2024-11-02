import os
import random
import requests
from ..config import OPENAI_API_KEY

def generate_background_image(prompts, photos_folder, max_retries=3):
    """
    Generates background image using song prompts as inspiration while maintaining cosmic café theme
    """
    # Extract mood and atmospheric words from the prompts
    mood_words = set()
    for title, prompt in prompts:
        words = prompt.lower().split()
        mood_words.update(word for word in words if word in {
            'mellow', 'warm', 'soft', 'gentle', 'relaxed', 'smooth', 'dreamy',
            'ambient', 'calm', 'serene', 'peaceful', 'tranquil', 'soothing'
        })
    
    base_elements = [
        "cozy café interior",
        "warm ambient lighting",
        "large windows"
    ]
    
    if mood_words:
        mood_description = f"with {', '.join(list(mood_words)[:3])} atmosphere"
        base_elements.append(mood_description)
    
    cosmic_elements = [
        "galaxy visible through windows",
        "floating nebulas in the distance",
        "gentle cosmic dust particles in the air",
        "aurora-like lights",
        "stars twinkling through glass ceiling",
        "ethereal space phenomena",
        "spiral galaxy reflections",
        "cosmic fog wisps",
        "floating constellation patterns",
        "subtle northern lights effect"
    ]
    
    cafe_elements = [
        "vintage record player",
        "steaming coffee cup",
        "potted plants",
        "wooden furniture",
        "soft Edison bulbs",
        "exposed brick walls",
        "hanging pendant lights",
        "vinyl records on walls",
        "cozy reading nook",
        "vintage jazz posters"
    ]
    
    selected_cosmic = random.sample(cosmic_elements, 2)
    selected_cafe = random.sample(cafe_elements, 2)
    elements = base_elements + selected_cosmic + selected_cafe
    sample_prompt = random.choice(prompts)[1]
    
    image_prompt = (
        f"Create a dreamy lofi café scene with cosmic elements: {', '.join(elements)}. "
        f"The atmosphere should match the mood of this music: '{sample_prompt}'. "
        "Digital art style with rich colors and atmospheric lighting. "
        "The scene should blend cozy café aesthetics with subtle sci-fi elements. "
        "4K quality, detailed, atmospheric, perfect for lofi music background. "
        "Style similar to Studio Ghibli meets cosmic art."
    )
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "dall-e-3",
        "prompt": image_prompt,
        "n": 1,
        "size": "1792x1024",
        "quality": "hd"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            image_url = response.json()['data'][0]['url']
            image_path = os.path.join(photos_folder, "background.jpg")
            
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Background image generated and saved as {image_path}")
                return image_path
            else:
                print(f"Failed to download the generated image on attempt {attempt + 1}")
                
        except Exception as e:
            print(f"Error generating image on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    
    default_image_path = "assets/default_background.jpg"
    if os.path.exists(default_image_path):
        print("Using default background image")
        import shutil
        backup_path = os.path.join(photos_folder, "background.jpg")
        shutil.copy2(default_image_path, backup_path)
        return backup_path
    else:
        raise FileNotFoundError("No default background image found and failed to generate new one")