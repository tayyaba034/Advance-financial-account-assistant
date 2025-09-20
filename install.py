"""
Installation script for Advanced Accounts Agent.
This script helps install all required dependencies.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print(f"❌ Python 3.12+ is required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install all required dependencies."""
    print("🚀 Advanced Accounts Agent - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Upgrade pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install the package in development mode
    if not run_command(f"{sys.executable} -m pip install -e .", "Installing Advanced Accounts Agent"):
        return False
    
    # Install additional dependencies that might be missing
    additional_deps = [
        "pydantic-settings",
        "google-generativeai",
        "fastapi",
        "uvicorn",
        "python-dotenv"
    ]
    
    for dep in additional_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Warning: Failed to install {dep}")
    
    print("\n🎉 Installation completed!")
    print("=" * 50)
    print("Next steps:")
    print("1. Run: python setup_env.py (to set up environment variables)")
    print("2. Run: python demo_mode.py (to see a demo)")
    print("3. Run: python main.py (to start the full application)")
    print("=" * 50)
    
    return True

def test_installation():
    """Test if the installation was successful."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import config
        import orchestrator
        import agents
        print("✅ All modules imported successfully!")
        
        # Test configuration
        from config import get_settings
        settings = get_settings()
        print(f"✅ Configuration loaded: {settings.app_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = install_dependencies()
    
    if success:
        test_installation()
    else:
        print("\n❌ Installation failed. Please check the errors above.")
        sys.exit(1)
