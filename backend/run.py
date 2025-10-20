#!/usr/bin/env python
"""
Convenience script to run the backend server.
Usage: python run.py
"""

import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 Starting Frontdesk AI Receptionist Backend...")
    print(f"📍 Server will run at http://{settings.api_host}:{settings.api_port}")
    print(f"📚 API docs available at http://{settings.api_host}:{settings.api_port}/docs")
    print(f"🔌 WebSocket endpoint: ws://{settings.api_host}:{settings.api_port}/ws")
    print("\n✨ Press CTRL+C to stop the server\n")
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
