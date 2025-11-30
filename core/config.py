
import os
from dotenv import load_dotenv

def load_env():
    """Loads environment variables from .env file."""
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("Environment loaded ✔")
    else:
        print("No .env file found — running without environment variables.")
