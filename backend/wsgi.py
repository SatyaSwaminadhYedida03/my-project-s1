"""
WSGI Entry Point for Vercel
"""
from app import app

# Vercel requires the app to be named 'app' or exposed via this file
if __name__ == "__main__":
    app.run()
