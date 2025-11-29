"""
main.py
-------
This module initializes and runs the FastAPI backend application for the Intrusion Detection System.
It exposes the REST endpoints that allow the frontend to control and retrieve real-time network capture data.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import packetRoutes

#----------------------------------------------------------------------------------------------------------------------
# Application Initialization
#----------------------------------------------------------------------------------------------------------------------

app = FastAPI(
    title="Intrusion Detection System Backend",
    description= "Backend application for the Intrusion Detection System, providing REST endpoints for network capture data.",
    version="1.0.0"
)

#------------------------------------------------------------------------------------------------------
# CORS Middleware Configuration
#------------------------------------------------------------------------------------------------------

origins = [
    "http://localhost:8080",  # Vite default dev server
    "http://127.0.0.1:8080",  # Also common
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production to specific origins  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#------------------------------------------------------------------------------------------------------
# Route Inclusion
#------------------------------------------------------------------------------------------------------

# Mount all packet-related routes from the dedicated route module
app.include_router(packetRoutes.router, prefix="/api/packets", tags=["Packet Operation"])

#------------------------------------------------------------------------------------------------------
# Root Endpoint
#------------------------------------------------------------------------------------------------------

@app.get("/")
async def root():
    """
    Root endpoint for service health check.
    Returns a basic JSON object to confirm backend availability.
    """
    return {"message": "Intrusion Detection System Backend is running."}

# -----------------------------------------------------------------------------------------------------
# Application Entrypoint
# -----------------------------------------------------------------------------------------------------

# This block allows running the app directly via "python main.py"
if __name__ == "__main__":
    import uvicorn
    # Start the ASGI server; host and port can be adjusted via .env configuration
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
