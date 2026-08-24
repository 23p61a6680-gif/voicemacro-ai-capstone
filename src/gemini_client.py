from google import genai
from google.genai import types
import json
from typing import Dict, Any, Optional
from src.config import get_api_key, GEMINI_MODEL

class GeminiClient:
    def __init__(self):
        self.api_key = get_api_key()
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            
    def is_configured(self) -> bool:
        return self.client is not None

    def generate_code_from_prompt(self, system_instruction: str, prompt: str) -> Optional[Dict[str, Any]]:
        if not self.is_configured():
            raise ValueError("Gemini API key is not configured.")
            
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.0, # Deterministic code generation
                    response_mime_type="application/json"
                )
            )
            
            # The model is configured to return JSON
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini response as JSON: {e}\nResponse text: {response.text}")
        except Exception as e:
            raise RuntimeError(f"Gemini API request failed: {e}")

    def generate_text_from_prompt(self, system_instruction: str, prompt: str) -> str:
        if not self.is_configured():
            raise ValueError("Gemini API key is not configured.")
            
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7 # A bit more creative for text explanations
                )
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API text generation failed: {e}")
