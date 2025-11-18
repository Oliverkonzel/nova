"""
Main Application Entry Point
Run this file to start the server: python main.py
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import webhooks, health
from config import HOST, PORT
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Nova Voice Agent",
    description="AI Voice Agent for Orbyn.ai",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("Nova Voice Agent Starting...")
    print("=" * 60)
    print(f"Twilio webhook: /webhooks/voice/incoming")
    print(f"Health check: /health")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    print("Nova shutting down...")

if __name__ == "__main__":
    print(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True
    )
