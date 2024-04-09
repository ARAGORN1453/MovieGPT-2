from pathlib import Path
import google.generativeai as genai
from apikey import *

genai.configure(api_key=google_gemini_api_key)

# Set up the model
generation_config_vision = {
  "temperature": 0.6,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_setting_vision = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]