# Business Automation Projects - Setup Guide

## 🚀 Quick Start

This guide will help you set up and run all the business automation projects in this portfolio.

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.9+** (for local development)
- **Node.js 16+** (for n8n workflows)
- **Git** (for version control)

## 🐳 Docker Setup (Recommended)

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd Client-protfolio
```

### 2. Environment Configuration
```bash
# Copy environment template
cp env.template .env

# Edit .env with your actual API keys and credentials
nano .env
```

### 3. Start All Services
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access Services
- **WhatsApp Bot**: http://localhost:5000
- **Email Bot**: http://localhost:8001
- **Real Estate Tool**: http://localhost:8002
- **n8n Workflows**: http://localhost:5678
- **Voice Bot**: http://localhost:8003
- **Xera Bot**: http://localhost:8004

## 🐍 Local Development Setup

### 1. Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install all project dependencies
pip install -r projects/whatsapp-automation-bot/requirements.txt
pip install -r projects/email-automation-bot/requirements.txt
pip install -r projects/real-estate-automation/requirements.txt
pip install -r projects/elevenlabs-voice-bot/requirements.txt
pip install -r projects/xera-business-bot/requirements.txt
```

### 3. Node.js Dependencies
```bash
# Install n8n globally
npm install -g n8n

# Install Xera bot dependencies
cd projects/xera-business-bot
npm install
```

### 4. Database Setup
```bash
# Start PostgreSQL (if using Docker)
docker run -d --name postgres \
  -e POSTGRES_DB=automation_db \
  -e POSTGRES_USER=automation \
  -e POSTGRES_PASSWORD=automation123 \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
docker run -d --name redis \
  -p 6379:6379 \
  redis:7-alpine

# Start MongoDB
docker run -d --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=automation \
  -e MONGO_INITDB_ROOT_PASSWORD=automation123 \
  -p 27017:27017 \
  mongo:6
```

## 🔧 Individual Project Setup

### WhatsApp Automation Bot
```bash
cd projects/whatsapp-automation-bot

# Set environment variables
export OPENAI_API_KEY="your_key_here"
export WHATSAPP_API_KEY="your_key_here"

# Run the bot
python app.py
```

### Email Automation Bot
```bash
cd projects/email-automation-bot

# Set environment variables
export OPENAI_API_KEY="your_key_here"
export EMAIL_SERVER="smtp.gmail.com"
export EMAIL_USERNAME="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"

# Run the bot
python main.py
```

### Real Estate Automation Tool
```bash
cd projects/real-estate-automation

# Set environment variables
export OPENAI_API_KEY="your_key_here"
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"

# Run Django
python manage.py migrate
python manage.py runserver
```

### n8n Workflow Automation
```bash
cd projects/n8n-workflows

# Set environment variables
export N8N_BASIC_AUTH_USER="admin"
export N8N_BASIC_AUTH_PASSWORD="secure_password"

# Start n8n
n8n start
```

### ElevenLabs Voice Bot
```bash
cd projects/elevenlabs-voice-bot

# Set environment variables
export ELEVENLABS_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"

# Run the bot
python main.py
```

### Xera Business Automation Bot
```bash
cd projects/xera-business-bot

# Set environment variables
export OPENAI_API_KEY="your_key_here"
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"

# Run Django
python manage.py migrate
python manage.py runserver
```

## 🔑 Required API Keys

### OpenAI
- Sign up at [OpenAI](https://openai.com/)
- Get API key from dashboard
- Add to `.env` file

### WhatsApp Business API
- Apply for [WhatsApp Business API](https://business.whatsapp.com/)
- Get API credentials
- Add to `.env` file

### ElevenLabs
- Sign up at [ElevenLabs](https://elevenlabs.io/)
- Get API key from dashboard
- Add to `.env` file

### Email Services
- Gmail: Enable 2FA and generate app password
- Or use SendGrid/Mailgun for production

## 📊 Monitoring & Health Checks

### Health Check Endpoints
- WhatsApp Bot: `GET /health`
- Email Bot: `GET /health`
- Voice Bot: `GET /health`
- Xera Bot: `GET /admin/`

### Logs
```bash
# View all container logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f whatsapp-bot
docker-compose logs -f email-bot
```

## 🚀 Production Deployment

### 1. Environment Variables
- Set `DEBUG=False`
- Use strong secret keys
- Configure production databases
- Set up SSL certificates

### 2. Reverse Proxy
- Use Nginx for load balancing
- Configure SSL termination
- Set up rate limiting

### 3. Monitoring
- Set up Prometheus + Grafana
- Configure alerting
- Monitor resource usage

### 4. Backup
- Regular database backups
- Configuration backups
- Log rotation

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>
```

#### Database Connection Issues
```bash
# Check if database is running
docker ps | grep postgres

# Restart database
docker-compose restart postgres
```

#### API Key Issues
- Verify API keys are correct
- Check API quotas and limits
- Ensure proper environment variable names

#### Permission Issues
```bash
# Fix file permissions
chmod +x projects/*/main.py
chmod +x projects/*/app.py
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [n8n Documentation](https://docs.n8n.io/)
- [ElevenLabs API Docs](https://elevenlabs.io/docs)

## 🤝 Support

For support and questions:
- **Email**: abidhamza579@gmail.com
- **Issues**: Create an issue in the repository
- **Documentation**: Check individual project READMEs

---

**Happy Automating! 🚀**

