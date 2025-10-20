"""
Voice Integration - Add real speech to the AI receptionist
This integrates Speech-to-Text and Text-to-Speech services
"""

import os
from typing import Optional
import asyncio

# Choose your services:
# Option 1: OpenAI (easiest, all-in-one)
# Option 2: Deepgram + ElevenLabs (best quality)
# Option 3: Google Cloud (enterprise)


# ============================================================
# OPTION 1: OpenAI (Easiest Setup)
# ============================================================

class OpenAIVoiceHandler:
    """
    Use OpenAI for both speech-to-text and text-to-speech.
    Requires: pip install openai
    """
    
    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        """
        Convert audio file to text using OpenAI Whisper.
        
        Args:
            audio_file_path: Path to audio file (mp3, wav, etc.)
        
        Returns:
            Transcribed text
        """
        with open(audio_file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    
    async def text_to_speech(self, text: str, output_path: str = "response.mp3") -> str:
        """
        Convert text to speech using OpenAI TTS.
        
        Args:
            text: Text to convert to speech
            output_path: Where to save the audio file
        
        Returns:
            Path to generated audio file
        """
        response = self.client.audio.speech.create(
            model="tts-1",  # or "tts-1-hd" for higher quality
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        response.stream_to_file(output_path)
        return output_path


# ============================================================
# OPTION 2: Deepgram + ElevenLabs (Best Quality)
# ============================================================

class DeepgramElevenLabsHandler:
    """
    Use Deepgram for STT and ElevenLabs for TTS.
    Requires: 
        pip install deepgram-sdk elevenlabs
    """
    
    def __init__(self, deepgram_key: str, elevenlabs_key: str):
        from deepgram import Deepgram
        from elevenlabs import set_api_key
        
        self.deepgram = Deepgram(deepgram_key)
        set_api_key(elevenlabs_key)
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        """Convert audio to text using Deepgram."""
        with open(audio_file_path, 'rb') as audio:
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            response = await self.deepgram.transcription.prerecorded(
                source,
                {'punctuate': True, 'language': 'en'}
            )
        
        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
        return transcript
    
    async def text_to_speech(self, text: str, output_path: str = "response.mp3") -> str:
        """Convert text to speech using ElevenLabs."""
        from elevenlabs import generate, save
        
        audio = generate(
            text=text,
            voice="Bella",  # Or other voices: Adam, Antoni, Arnold, etc.
            model="eleven_monolingual_v1"
        )
        
        save(audio, output_path)
        return output_path


# ============================================================
# OPTION 3: Google Cloud (Enterprise)
# ============================================================

class GoogleCloudVoiceHandler:
    """
    Use Google Cloud for both STT and TTS.
    Requires: 
        pip install google-cloud-speech google-cloud-texttospeech
    """
    
    def __init__(self, credentials_path: str):
        from google.cloud import speech, texttospeech
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.speech_client = speech.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()
    
    async def speech_to_text(self, audio_file_path: str) -> str:
        """Convert audio to text using Google Speech-to-Text."""
        from google.cloud import speech
        
        with open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()
        
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
        )
        
        response = self.speech_client.recognize(config=config, audio=audio)
        
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript
        
        return transcript
    
    async def text_to_speech(self, text: str, output_path: str = "response.mp3") -> str:
        """Convert text to speech using Google Text-to-Speech."""
        from google.cloud import texttospeech
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",  # Female voice
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open(output_path, 'wb') as out:
            out.write(response.audio_content)
        
        return output_path


# ============================================================
# USAGE EXAMPLE
# ============================================================

async def example_usage():
    """Example of how to use voice integration."""
    
    # Option 1: OpenAI (Easiest)
    openai_key = os.getenv('OPENAI_API_KEY')
    voice_handler = OpenAIVoiceHandler(openai_key)
    
    # Customer speaks (audio file from LiveKit)
    customer_audio = "customer_question.mp3"
    question_text = await voice_handler.speech_to_text(customer_audio)
    print(f"Customer asked: {question_text}")
    
    # AI processes and generates response
    ai_response = "We're open Monday-Saturday 9 AM - 8 PM."
    
    # Convert AI response to speech
    response_audio = await voice_handler.text_to_speech(ai_response)
    print(f"AI response saved to: {response_audio}")
    
    # Play audio back to customer via LiveKit
    # (See livekit_real.py for integration)


# ============================================================
# INTEGRATION WITH EXISTING SYSTEM
# ============================================================

"""
To integrate with your existing system:

1. Install dependencies:
   pip install openai  # For OpenAI option
   # OR
   pip install deepgram-sdk elevenlabs  # For Deepgram + ElevenLabs
   # OR
   pip install google-cloud-speech google-cloud-texttospeech  # For Google

2. Update ai_agent.py to use voice:

   from voice_integration import OpenAIVoiceHandler
   
   voice_handler = OpenAIVoiceHandler(settings.openai_api_key)
   
   # In process_question method:
   async def process_question(self, audio_file: str, customer_id: str):
       # Convert speech to text
       question = await voice_handler.speech_to_text(audio_file)
       
       # Process with AI (existing logic)
       result = await self.process_question(question, customer_id)
       
       # Convert response to speech
       audio_response = await voice_handler.text_to_speech(result['response'])
       
       return {
           'response_text': result['response'],
           'response_audio': audio_response,
           'needs_help': result['needs_help']
       }

3. Update livekit_handler.py to stream audio:
   - Receive audio stream from customer
   - Save to temp file
   - Pass to voice_handler.speech_to_text()
   - Get AI response
   - Convert to speech
   - Stream back to customer
"""


# ============================================================
# RECOMMENDED SETUP FOR YOUR PROJECT
# ============================================================

"""
RECOMMENDED: Use OpenAI for everything (simplest)

1. Add to requirements.txt:
   openai>=1.12.0

2. Already have OPENAI_API_KEY in .env ✅

3. Usage:
   - Speech-to-Text: OpenAI Whisper (included)
   - Text-to-Speech: OpenAI TTS (included)
   - AI Logic: OpenAI GPT-4 (already using)
   
4. Cost:
   - Whisper: $0.006 per minute
   - TTS: $0.015 per 1K characters
   - GPT-4: $0.03 per 1K tokens
   
   Example: 2-minute call = ~$0.05 total

5. Quality:
   - Whisper: Excellent accuracy
   - TTS: Natural sounding
   - GPT-4: Best AI responses
"""

if __name__ == "__main__":
    # Test the voice handler
    asyncio.run(example_usage())
