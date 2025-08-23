#!/usr/bin/env python3
"""
WhatsApp Automation Bot
A comprehensive business automation solution for WhatsApp
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class WhatsAppBot:
    def __init__(self):
        self.conversation_history = {}
        self.faq_database = self.load_faq_database()
    
    def load_faq_database(self):
        """Load FAQ database from JSON file"""
        try:
            with open('faq_database.json', 'r') as f:
                return json.load(f)
            except FileNotFoundError:
                return {
                    "general": [
                        {"question": "What are your business hours?", "answer": "We're open 24/7 for online support!"},
                        {"question": "How can I contact support?", "answer": "You can reach us through this WhatsApp number or email us at support@company.com"}
                    ]
                }
    
    def generate_response(self, message, user_id):
        """Generate intelligent response using OpenAI"""
        try:
            # Build conversation context
            context = self.get_conversation_context(user_id, message)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful business assistant. Be professional, friendly, and concise."},
                    {"role": "user", "content": context}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            self.update_conversation_history(user_id, message, response_text)
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again later."
    
    def get_conversation_context(self, user_id, current_message):
        """Get conversation context for better responses"""
        if user_id in self.conversation_history:
            recent_messages = self.conversation_history[user_id][-5:]  # Last 5 messages
            context = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in recent_messages])
            return f"{context}\nUser: {current_message}"
        return f"User: {current_message}"
    
    def update_conversation_history(self, user_id, user_message, bot_response):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'user': user_message,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 messages
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]

# Initialize bot
bot = WhatsAppBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for WhatsApp messages"""
    try:
        data = request.get_json()
        logger.info(f"Received webhook data: {data}")
        
        # Extract message details
        message = data.get('message', {})
        user_id = message.get('from', 'unknown')
        text = message.get('text', {}).get('body', '')
        
        if text:
            # Generate response
            response = bot.generate_response(text, user_id)
            
            # Log interaction
            logger.info(f"User {user_id}: {text}")
            logger.info(f"Bot response: {response}")
            
            return jsonify({
                'status': 'success',
                'response': response,
                'user_id': user_id
            })
        
        return jsonify({'status': 'success', 'message': 'No text message received'})
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'WhatsApp Automation Bot'
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get bot statistics"""
    total_conversations = len(bot.conversation_history)
    total_messages = sum(len(conv) for conv in bot.conversation_history.values())
    
    return jsonify({
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'active_users': len([conv for conv in bot.conversation_history.values() if conv])
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
