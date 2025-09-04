#!/usr/bin/env python3
"""
Development setup script for Pestozap Backend
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Pestozap Backend for development...")
    
    # Check if .env exists
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("📋 Creating .env from .env.example...")
            try:
                with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                    dst.write(src.read())
                print("✅ .env file created")
            except Exception as e:
                print(f"❌ Failed to create .env: {e}")
                return False
        else:
            print("❌ .env.example not found")
            return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    
    if not run_command("python manage.py migrate", "Running migrations"):
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Visit: http://localhost:8000/admin/")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)