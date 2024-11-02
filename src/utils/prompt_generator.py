from ..config import anthropic_client

def get_prompts_from_gpt():
    """
    Fetches 15 unique lofi jazz prompts from Claude.
    """
    prompt = """
    You are tasked with generating unique prompts for smooth lofi jazz songs that will be used with SunoAI, a Prompt To Music generator. Your goal is to create a table of prompts, each with a creative title and a corresponding prompt that describes the style and topic of the song.

    Follow these guidelines when creating the prompts:
    1. Focus on describing the style of music and the topic or mood of the song.
    2. Use genres, sub-genres, and vibes instead of referencing specific artists or songs.
    3. Incorporate various instruments, tempos, and atmospheric elements commonly associated with lofi jazz.
    4. Include diverse themes and emotions to ensure a wide range of unique prompts.
    5. Keep the prompts concise but descriptive, typically 20-40 words each.

    Create a table with two columns: "Title" and "Prompt". Generate 15 unique entries, ensuring that each prompt is distinct and creative.

    To generate the prompts:
    1. Think about different moods, settings, and emotions that can be expressed through lofi jazz.
    2. Consider various instruments and sound elements that are characteristic of the genre.
    3. Imagine unique scenarios or themes that could inspire a lofi jazz composition.
    4. Combine these elements to create a cohesive and evocative prompt.

    Here are some examples of good prompts:

    "A chill lofi jazz track featuring soft saxophone, mellow electric piano, and ambient coffee shop background sounds, evoking the comforting warmth of a late-night café."

    "Lofi jazz with a relaxed beat, warm electric piano, and subtle synths, evoking the serene yet vibrant atmosphere of a late-night urban cityscape."

    "Relaxed lofi jazz with soothing vibraphone, light percussive brushes, and gentle electric piano, creating a calm, reflective mood for a cloudy afternoon."

    Present your output in the following format:

    <table>
    | Title | Prompt |
    |-------|--------|
    | [Title 1] | [Prompt 1] |
    | [Title 2] | [Prompt 2] |
    ...
    | [Title 15] | [Prompt 15] |
    </table>

    Ensure that your table contains exactly 15 rows of unique lofi jazz song prompts. Be creative and diverse in your suggestions, covering a wide range of moods, themes, and musical elements within the lofi jazz genre.
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
    print("Received prompts from Claude:\n", content)

    # Updated parsing logic
    titles_and_prompts = []
    for line in content.splitlines():
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 3:  # Valid table row should have at least 3 parts
                title = parts[1].strip()
                prompt = parts[2].strip()
                if prompt and prompt != 'Prompt' and not all(c in '-' for c in prompt):
                    titles_and_prompts.append((title, prompt))
    
    return titles_and_prompts