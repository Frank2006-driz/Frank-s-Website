"""
Configuration settings for the Flask application.
Customize these values for different environments.
"""

import os
from datetime import timedelta

# Application Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
DEBUG = os.environ.get('FLASK_ENV', 'development') == 'development'
TESTING = os.environ.get('TESTING', False)

# Database Settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///website.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = DEBUG

# Session Settings
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_COOKIE_SECURE = not DEBUG  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# File Upload Settings (if you add file uploads)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Email Settings (if you add email functionality)
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# Pagination
ITEMS_PER_PAGE = 10

# Logging
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
