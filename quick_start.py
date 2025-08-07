#!/usr/bin/env python3
"""
Quick Start Script for Movie Recommendation System
Choose between Flask and Streamlit versions
"""

import subprocess
import sys
import os
import time

def print_banner():
    """Print the application banner"""
    print("🎬" * 20)
    print("🎬 Movie Recommendation System 🎬")
    print("🎬" * 20)
    print()

def check_files():
    """Check if required files exist"""
    required_files = [
        "recommendation_system.py",
        "data/movies.csv",
        "data/ratings.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def run_flask():
    """Run the Flask version"""
    print("🌐 Starting Flask Web Application...")
    print("📍 URL: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Flask app stopped")

def run_streamlit():
    """Run the Streamlit version"""
    print("📱 Starting Streamlit Application...")
    print("📍 URL: http://localhost:8501")
    print("🔄 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        subprocess.run(["streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped")
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed! Please run the script again.")

def run_demo():
    """Run the demo script"""
    print("🎯 Running Demo Script...")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "demo.py"])
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped")

def main():
    print_banner()
    
    # Check files
    if not check_files():
        print("\n❌ Please make sure all required files are present.")
        return
    
    print("\n🚀 Choose an option:")
    print("1. 🌐 Flask Web App (Traditional web interface)")
    print("2. 📱 Streamlit App (Modern interactive interface)")
    print("3. 🎯 Run Demo (Command line demo)")
    print("4. 📊 View Project Info")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                run_flask()
                break
            elif choice == "2":
                run_streamlit()
                break
            elif choice == "3":
                run_demo()
                break
            elif choice == "4":
                show_project_info()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

def show_project_info():
    """Show project information"""
    print("\n📊 Project Information:")
    print("=" * 40)
    print("🎬 Movie Recommendation System")
    print("📅 Created: 2025")
    print("🔧 Technologies: Python, Flask, Streamlit, scikit-learn")
    print("📁 Files:")
    
    files = [
        ("recommendation_system.py", "Core recommendation engine"),
        ("app.py", "Flask web application"),
        ("streamlit_app.py", "Streamlit web application"),
        ("demo.py", "Command line demo"),
        ("data/movies.csv", "Movie dataset (100 movies)"),
        ("data/ratings.csv", "User ratings dataset"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Project documentation")
    ]
    
    for file, description in files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"   {status} {file} - {description}")
    
    print("\n🎯 Features:")
    print("   • Content-Based Filtering")
    print("   • Collaborative Filtering")
    print("   • Hybrid Recommendations")
    print("   • Movie Search")
    print("   • Analytics Dashboard")
    print("   • Interactive Visualizations")
    
    print("\n📈 Dataset:")
    print("   • 100 movies (1972-2025)")
    print("   • 20 users with ratings")
    print("   • 15+ different genres")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 