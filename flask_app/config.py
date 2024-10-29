import os
import urllib.parse

# Stores all configuration values
SECRET_KEY = os.urandom(24)  # 24 bytes for a sufficiently strong key
# MongoDB Connection String (encode special characters in your password)
password = urllib.parse.quote_plus("xzco5qXYweAd5GYt")  # Encode the password to handle any special characters
MONGODB_HOST = f'mongodb+srv://affan:{password}@timeline.2xid5.mongodb.net/'

#Also configure Flask-Mail in routes.py or comment out