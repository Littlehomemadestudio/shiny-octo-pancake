"""
Setup script for World War Telegram Bot
"""
import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Requirements installed successfully!")

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as src:
                with open(".env", "w") as dst:
                    dst.write(src.read())
            print("✅ Created .env file from template")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")

def check_config():
    """Check if config.json exists"""
    if not os.path.exists("config.json"):
        print("❌ config.json not found. Please create it from the template.")
        return False
    print("✅ config.json found")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up World War Telegram Bot...")
    print()
    
    # Install requirements
    install_requirements()
    print()
    
    # Create .env file
    create_env_file()
    print()
    
    # Check config
    if not check_config():
        print("❌ Setup incomplete. Please create config.json")
        return
    
    print("✅ Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file with your bot token and database URL")
    print("2. Edit config.json with your game settings")
    print("3. Set up your PostgreSQL database")
    print("4. Run: python main.py")
    print()
    print("For more information, see README.md")

if __name__ == "__main__":
    main()