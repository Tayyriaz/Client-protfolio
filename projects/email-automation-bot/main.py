#!/usr/bin/env python3
"""
Email Automation Bot
AI-powered email automation for customer support and follow-ups
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Email Automation Bot",
    description="AI-powered email automation for business",
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

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    content: str
    priority: str = "normal"
    category: str = "general"

class EmailResponse(BaseModel):
    message_id: str
    status: str
    timestamp: datetime
    ai_generated: bool

class EmailBot:
    def __init__(self):
        self.email_history = {}
        self.categories = {
            "support": "Customer support inquiries",
            "sales": "Sales and lead generation",
            "billing": "Billing and payment issues",
            "general": "General inquiries"
        }
    
    def categorize_email(self, subject: str, content: str) -> str:
        """Categorize email using AI"""
        try:
            prompt = f"Subject: {subject}\nContent: {content[:500]}\n\nCategorize this email into one of these categories: {', '.join(self.categories.keys())}. Return only the category name."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an email categorization expert. Return only the category name."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            category = response.choices[0].message.content.strip().lower()
            return category if category in self.categories else "general"
            
        except Exception as e:
            logger.error(f"Error categorizing email: {e}")
            return "general"
    
    def generate_response(self, email_content: str, category: str) -> str:
        """Generate AI-powered email response"""
        try:
            system_prompt = f"You are a professional customer service representative. Generate a helpful, professional response for a {category} email. Keep it concise and friendly."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": email_content}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Thank you for your email. We will get back to you shortly."

# Initialize bot
bot = EmailBot()

@app.post("/send-email", response_model=EmailResponse)
async def send_email(email_req: EmailRequest, background_tasks: BackgroundTasks):
    """Send automated email"""
    try:
        # Categorize email
        category = bot.categorize_email(email_req.subject, email_req.content)
        
        # Generate AI response if needed
        if email_req.content.lower().startswith("auto"):
            ai_response = bot.generate_response(email_req.content, category)
            email_req.content = ai_response
        
        # Send email (simulated for demo)
        message_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store in history
        bot.email_history[message_id] = {
            "to": email_req.to_email,
            "subject": email_req.subject,
            "content": email_req.content,
            "category": category,
            "priority": email_req.priority,
            "timestamp": datetime.now(),
            "ai_generated": email_req.content.lower().startswith("auto")
        }
        
        # Background task for actual email sending
        background_tasks.add_task(send_email_task, email_req)
        
        return EmailResponse(
            message_id=message_id,
            status="sent",
            timestamp=datetime.now(),
            ai_generated=email_req.content.lower().startswith("auto")
        )
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def send_email_task(email_req: EmailRequest):
    """Background task to send email"""
    # Simulate email sending
    await asyncio.sleep(1)
    logger.info(f"Email sent to {email_req.to_email}")

@app.get("/email-stats")
async def get_email_stats():
    """Get email statistics"""
    total_emails = len(bot.email_history)
    ai_generated = sum(1 for email in bot.email_history.values() if email["ai_generated"])
    
    category_counts = {}
    for email in bot.email_history.values():
        cat = email["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return {
        "total_emails": total_emails,
        "ai_generated": ai_generated,
        "category_distribution": category_counts,
        "last_24h": len([e for e in bot.email_history.values() 
                         if e["timestamp"] > datetime.now() - timedelta(days=1)])
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Email Automation Bot"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
