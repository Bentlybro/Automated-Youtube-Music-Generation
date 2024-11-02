import os
from anthropic import Anthropic

# API Keys and Configuration
ANTHROPIC_API_KEY = 'ANTHROPIC_API_KEY'
OPENAI_API_KEY = 'OPENAI_API_KEY'
BASE_URL = 'http://localhost:3000'

# Initialize clients
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# YouTube API Configuration
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
YOUTUBE_API_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"