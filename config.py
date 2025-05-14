import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # Try to get API key from environment variable, fall back to hardcoded value if not found
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBf_C_bV9mPzvwOkwI9Hqzyxx_6QJdPYc8')
    
    # Add other configuration variables as needed
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5002))
    HOST = os.environ.get('HOST', '0.0.0.0') 