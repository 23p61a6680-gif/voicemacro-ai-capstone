from google import genai
from google.genai import types
from src.config import get_api_key, GEMINI_MODEL

class AudioProcessor:
    def __init__(self):
        self.api_key = get_api_key()
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def transcribe_audio(self, audio_bytes: bytes, mime_type: str = "audio/wav") -> str:
        """
        Uses Gemini's multimodal capabilities to transcribe the audio command.
        """
        if not self.client:
            raise ValueError("Gemini API key is not configured.")
            
        prompt = "Please accurately transcribe the spoken command in this audio. Only output the transcription, nothing else."
        
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                    prompt
                ]
            )
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Audio transcription failed: {e}")
