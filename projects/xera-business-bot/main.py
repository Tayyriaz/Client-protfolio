#!/usr/bin/env python3
"""
Xera Business Automation Bot
Main Django application for business process automation
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xera_bot.settings')

# Setup Django
django.setup()

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
