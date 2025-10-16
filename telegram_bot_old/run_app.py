#!/usr/bin/env python3
"""
Quran Reader App Launcher
Simple launcher script for the Enhanced Quran Reader Application
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PIL
        import sqlite3
        return True
    except ImportError as e:
        return False, str(e)

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main launcher function"""
    print("🕌 Enhanced Quran Reader App Launcher")
    print("=" * 40)
    
    # Check dependencies
    print("Checking dependencies...")
    deps_check = check_dependencies()
    
    if deps_check is not True:
        print(f"❌ Missing dependencies: {deps_check[1] if isinstance(deps_check, tuple) else deps_check}")
        print("Installing dependencies...")
        
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("pip install -r requirements.txt")
            return
        
        print("✅ Dependencies installed successfully!")
    
    print("✅ All dependencies are available!")
    
    # Check if main app file exists
    if not os.path.exists("improved_quran_app.py"):
        print("❌ Main application file not found!")
        print("Please ensure 'improved_quran_app.py' is in the same directory.")
        return
    
    print("🚀 Starting Quran Reader App...")
    
    try:
        # Import and run the main application
        from improved_quran_app import main as run_app
        run_app()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        
        # Show error dialog
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Error", f"Failed to start the application:\n{e}")
        root.destroy()

if __name__ == "__main__":
    main()