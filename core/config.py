
from google.genai import types

APP_NAME = "ecc"

# Model we working with 
MODEL_NAME = "gemini-2.0-flash"

# Basic retry cinfig for robustness
RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=5,
    initial_delay=1,
    exp_base=2,
    http_status_codes=[429, 500, 503, 504],
)

