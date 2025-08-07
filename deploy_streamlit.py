#!/usr/bin/env python3
"""
Deployment script for the Streamlit Movie Recommendation System
This script helps you run the Streamlit app with different configurations
"""

import subprocess
import sys
import os
import argparse

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'plotly', 'pandas', 'numpy', 'scikit-learn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ All packages installed successfully!")
    else:
        print("✅ All required packages are installed!")

def run_streamlit(port=8501, host="localhost", headless=False):
    """Run the Streamlit app with specified configuration"""
    cmd = [
        "streamlit", "run", "streamlit_app.py",
        "--server.port", str(port),
        "--server.address", host
    ]
    
    if headless:
        cmd.extend(["--server.headless", "true"])
    
    print(f"🚀 Starting Streamlit app...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit app stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

def main():
    parser = argparse.ArgumentParser(description="Deploy Streamlit Movie Recommendation System")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the app on (default: 8501)")
    parser.add_argument("--host", default="localhost", help="Host to run the app on (default: localhost)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--check-deps", action="store_true", help="Check and install dependencies")
    
    args = parser.parse_args()
    
    print("🎬 Movie Recommendation System - Streamlit Deployment")
    print("=" * 60)
    
    # Check if streamlit_app.py exists
    if not os.path.exists("streamlit_app.py"):
        print("❌ streamlit_app.py not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Check dependencies if requested
    if args.check_deps:
        check_dependencies()
    
    # Run the app
    run_streamlit(args.port, args.host, args.headless)

if __name__ == "__main__":
    main() 