"""
Environment setup script for Advanced Accounts Agent.
This script helps you create the .env file with the required environment variables.
"""

import os

def create_env_file():
    """Create a .env file with the required environment variables."""
    
    print("🔧 Advanced Accounts Agent - Environment Setup")
    print("=" * 50)
    
    # Get user input for environment variables
    google_api_key = input("Enter your Google AI Studio API Key: ").strip()
    xero_client_id = input("Enter your Xero Client ID: ").strip()
    xero_client_secret = input("Enter your Xero Client Secret: ").strip()
    xero_tenant_id = input("Enter your Xero Tenant ID (optional, press Enter to skip): ").strip()
    
    # Create .env file content
    env_content = f"""# Google AI Studio Configuration
GOOGLE_AI_STUDIO_API_KEY={google_api_key}
GOOGLE_AI_MODEL=gemini-1.5-flash

# Xero Configuration
XERO_CLIENT_ID={xero_client_id}
XERO_CLIENT_SECRET={xero_client_secret}
XERO_TENANT_ID={xero_tenant_id}

# Application Configuration
APP_NAME=Advanced Accounts Agent
APP_VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Agent Configuration
MAX_RETRIES=3
TIMEOUT_SECONDS=30
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print("You can now run the application with: python main.py")
        
    except Exception as e:
        print(f"\n❌ Error creating .env file: {str(e)}")
        print("\nPlease create the .env file manually with the following content:")
        print("-" * 50)
        print(env_content)
        print("-" * 50)

def show_env_template():
    """Show the environment template without creating a file."""
    print("📋 Environment Variables Template")
    print("=" * 50)
    print("Create a .env file in the project root with the following content:")
    print()
    print("# Google AI Studio Configuration")
    print("GOOGLE_AI_STUDIO_API_KEY=your_google_ai_studio_api_key_here")
    print("GOOGLE_AI_MODEL=gemini-1.5-flash")
    print()
    print("# Xero Configuration")
    print("XERO_CLIENT_ID=your_xero_client_id_here")
    print("XERO_CLIENT_SECRET=your_xero_client_secret_here")
    print("XERO_TENANT_ID=your_xero_tenant_id_here")
    print()
    print("# Application Configuration")
    print("APP_NAME=Advanced Accounts Agent")
    print("APP_VERSION=1.0.0")
    print("DEBUG=false")
    print("HOST=0.0.0.0")
    print("PORT=8000")
    print()
    print("# Agent Configuration")
    print("MAX_RETRIES=3")
    print("TIMEOUT_SECONDS=30")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Interactive setup (create .env file)")
    print("2. Show template only")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        create_env_file()
    elif choice == "2":
        show_env_template()
    else:
        print("Invalid choice. Showing template...")
        show_env_template()
