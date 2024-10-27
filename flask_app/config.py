import os
import urllib.parse

# Stores all configuration values
#SECRET_KEY = b''

SECRET_KEY = os.urandom(24)  # 24 bytes for a sufficiently strong key
# MongoDB Connection String (encode special characters in your password)
password = urllib.parse.quote_plus("")  # Encode the password to handle any special characters
MONGODB_HOST = f''


#Also configure Flask-Mail in routes.py or comment out