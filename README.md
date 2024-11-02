# Automated-Youtube-Music-Generation

An automated system that generates, combines, and uploads lofi jazz music videos to youtube using AI. The system uses Claude AI for prompts, Suno AI for music generation, DALL-E for background images, and automatically uploads the final compilation to YouTube.

## Features

- 🎵 Generates unique lofi jazz songs using AI
- 🖼️ Creates themed background images with cosmic café aesthetics
- 📝 Generates video titles and descriptions
- 🎬 Compiles music into a single video
- 📤 Automatically uploads to YouTube with timestamps

## Prerequisites

- Python 3.9+
- Node.js and npm (for Suno API server)
- YouTube API credentials
- API keys for:
  - Anthropic (Claude)
  - OpenAI (DALL-E)
  - Suno AI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bentlybro/Automated-Youtube-Music-Generation.git
cd Automated-Youtube-Music-Generation
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your configuration:
   - Create a copy of `src/config-example.py` and name it `config.py`
   - Add your API keys and configuration:
```python
ANTHROPIC_API_KEY = 'your-claude-api-key'
OPENAI_API_KEY = 'your-openai-api-key'
BASE_URL = 'http://localhost:3000'  # Suno API server endpoint
```

4. Set up YouTube credentials:
   - Create a project in Google Cloud Console
   - Enable YouTube Data API v3
   - Download OAuth 2.0 credentials as `client_secrets.json`
   - Place in project root directory

5. Set up Suno API server:
   - Clone [gcui-art/suno-api](https://github.com/gcui-art/suno-api)
   - Follow their instructions to set up the server

## Usage

1. Start the Suno API server:
```bash
cd suno-api
npm run dev
```

2. Run the generator:
```bash
python main.py
```

The program will:
1. Generate multiple lofi jazz prompts using Claude
2. Create unique songs using Suno AI (2 variations per prompt)
3. Generate a cosmic café themed background image
4. Combine the songs into a single video
5. Upload the final video to YouTube

## Project Structure

```
src/
├── audio/
│   ├── generator.py    # Handles music generation via Suno AI
│   └── processor.py    # Processes and combines audio files
├── image/
│   └── generator.py    # Creates background images using DALL-E
├── video/
│   └── creator.py      # Combines audio and image into video
├── youtube/
│   └── uploader.py     # Handles YouTube upload and metadata
└── utils/
    ├── file_manager.py    # Manages file organization
    └── prompt_generator.py # Generates music prompts via Claude

Output/
├── YYYYMMDD_HHMMSS/
    ├── music/
    │   ├── segments/
    │   │   └── [prompt_folders]/
    │   └── combined_playlist.mp3
    ├── photos/
    │   └── background.jpg
    └── videos/
        └── playlist_video.mp4
```

## Process Flow

1. **Initialization & Prompt Generation**
   - Creates timestamped output folders
   - Uses Claude AI to generate unique lofi jazz prompts with titles and descriptions

2. **Content Generation**
   - Processes prompts concurrently (default: 3 at a time)
   - Generates music variations using Suno AI
   - Creates themed background image using DALL-E
   - Combines audio files into a single playlist
   - Creates final video with background image

3. **YouTube Upload**
   - Generates SEO-friendly titles and descriptions
   - Handles authentication and upload
   - Includes timestamps in video description

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Anthropic Claude](https://www.anthropic.com/claude) for prompt generation
- [Suno AI](https://suno.ai) for music generation
- [gcui-art/suno-api](https://github.com/gcui-art/suno-api) for Suno AI implementation
- [DALL-E](https://openai.com/dall-e-3) for image generation