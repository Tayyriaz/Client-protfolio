#!/usr/bin/env python3
"""
ElevenLabs Voice Bot
Advanced voice-enabled bot for customer engagement
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import elevenlabs
import openai
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime, timedelta
import asyncio
import tempfile
import uuid

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ElevenLabs Voice Bot",
    description="AI-powered voice bot for customer engagement",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure APIs
elevenlabs.set_api_key(os.getenv('ELEVENLABS_API_KEY'))
openai.api_key = os.getenv('OPENAI_API_KEY')

class VoiceRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Default voice
    language: str = "en"
    speed: float = 1.0
    emotion: str = "neutral"

class VoiceResponse(BaseModel):
    audio_url: str
    duration: float
    text: str
    voice_id: str
    timestamp: datetime

class VoiceBot:
    def __init__(self):
        self.voice_history = {}
        self.available_voices = self.load_voices()
        self.language_support = {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ar": "Arabic",
            "zh": "Chinese",
            "ja": "Japanese"
        }
    
    def load_voices(self):
        """Load available voices from ElevenLabs"""
        try:
            voices = elevenlabs.voices()
            return {voice.voice_id: voice.name for voice in voices}
        except Exception as e:
            logger.error(f"Error loading voices: {e}")
            return {
                "21m00Tcm4TlvDq8ikWAM": "Rachel",
                "AZnzlk1XvdvUeBnXmlld": "Domi",
                "EXAVITQu4vr4xnSDxMaL": "Bella"
            }
    
    def generate_voice(self, text: str, voice_id: str, speed: float = 1.0) -> bytes:
        """Generate voice using ElevenLabs"""
        try:
            audio = elevenlabs.generate(
                text=text,
                voice=voice_id,
                model="eleven_monolingual_v1"
            )
            return audio
        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            raise HTTPException(status_code=500, detail="Voice generation failed")
    
    def process_text(self, text: str, language: str) -> str:
        """Process text for voice generation"""
        try:
            # Use OpenAI to improve text for voice
            if language != "en":
                prompt = f"Translate this text to {self.language_support.get(language, 'English')} and make it natural for voice synthesis: {text}"
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a language expert. Translate and optimize text for natural voice synthesis."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                return response.choices[0].message.content
            return text
            
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return text

# Initialize bot
bot = VoiceBot()

@app.post("/generate-voice", response_model=VoiceResponse)
async def generate_voice(request: VoiceRequest, background_tasks: BackgroundTasks):
    """Generate voice from text"""
    try:
        # Process text
        processed_text = bot.process_text(request.text, request.language)
        
        # Generate voice
        audio_data = bot.generate_voice(processed_text, request.voice_id, request.speed)
        
        # Save audio file
        audio_id = str(uuid.uuid4())
        audio_path = f"/tmp/voice_{audio_id}.mp3"
        
        with open(audio_path, "wb") as f:
            f.write(audio_data)
        
        # Store in history
        bot.voice_history[audio_id] = {
            "text": processed_text,
            "voice_id": request.voice_id,
            "language": request.language,
            "speed": request.speed,
            "emotion": request.emotion,
            "timestamp": datetime.now(),
            "file_path": audio_path
        }
        
        # Clean up old files in background
        background_tasks.add_task(cleanup_old_files)
        
        return VoiceResponse(
            audio_url=f"/audio/{audio_id}",
            duration=len(audio_data) / 16000,  # Approximate duration
            text=processed_text,
            voice_id=request.voice_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error generating voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{audio_id}")
async def get_audio(audio_id: str):
    """Get generated audio file"""
    if audio_id not in bot.voice_history:
        raise HTTPException(status_code=404, detail="Audio not found")
    
    audio_info = bot.voice_history[audio_id]
    return FileResponse(
        audio_info["file_path"],
        media_type="audio/mpeg",
        filename=f"voice_{audio_id}.mp3"
    )

@app.get("/voices")
async def get_available_voices():
    """Get available voices"""
    return {
        "voices": bot.available_voices,
        "languages": bot.language_support,
        "total_voices": len(bot.available_voices)
    }

@app.get("/voice-stats")
async def get_voice_stats():
    """Get voice generation statistics"""
    total_generations = len(bot.voice_history)
    language_counts = {}
    voice_counts = {}
    
    for generation in bot.voice_history.values():
        lang = generation["language"]
        voice = generation["voice_id"]
        language_counts[lang] = language_counts.get(lang, 0) + 1
        voice_counts[voice] = voice_counts.get(voice, 0) + 1
    
    return {
        "total_generations": total_generations,
        "language_distribution": language_counts,
        "voice_distribution": voice_counts,
        "last_24h": len([g for g in bot.voice_history.values() 
                         if g["timestamp"] > datetime.now() - timedelta(days=1)])
    }

async def cleanup_old_files():
    """Clean up old audio files"""
    try:
        current_time = datetime.now()
        to_delete = []
        
        for audio_id, info in bot.voice_history.items():
            if (current_time - info["timestamp"]).days > 1:  # Keep for 1 day
                to_delete.append(audio_id)
        
        for audio_id in to_delete:
            try:
                os.remove(bot.voice_history[audio_id]["file_path"])
                del bot.voice_history[audio_id]
            except:
                pass
                
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ElevenLabs Voice Bot",
        "voices_available": len(bot.available_voices)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
