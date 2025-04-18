"""
Server module for running the FastAPI application with uvicorn.
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get host and port from environment variables or use defaults
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", "8000"))

if __name__ == "__main__":
    """Run the FastAPI application with uvicorn."""
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )
