"""
Debug script to check environment variable loading.
"""

import os
from dotenv import load_dotenv

print("🔍 Debugging Environment Variables")
print("=" * 50)

# Load .env file
load_dotenv()

print("📁 Current directory:", os.getcwd())
print("📄 .env file exists:", os.path.exists('.env'))

if os.path.exists('.env'):
    print("\n📄 .env file contents:")
    with open('.env', 'r') as f:
        for i, line in enumerate(f, 1):
            print(f"  {i}: {repr(line)}")

print("\n🔑 Environment variables:")
env_vars = [
    'GOOGLE_AI_STUDIO_API_KEY',
    'XERO_CLIENT_ID', 
    'XERO_CLIENT_SECRET'
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        # Show first 10 characters for security
        display_value = value[:10] + "..." if len(value) > 10 else value
        print(f"  ✅ {var}: {display_value}")
    else:
        print(f"  ❌ {var}: Not found")

print("\n🧪 Testing config loading:")
try:
    from config import get_settings, validate_environment
    settings = get_settings()
    print(f"  Settings loaded: {settings.app_name}")
    print(f"  Google AI Key length: {len(settings.google_ai_api_key)}")
    print(f"  Xero Client ID length: {len(settings.xero_client_id)}")
    print(f"  Xero Client Secret length: {len(settings.xero_client_secret)}")
    
    is_valid = validate_environment()
    print(f"  Environment valid: {is_valid}")
    
except Exception as e:
    print(f"  ❌ Error: {str(e)}")
