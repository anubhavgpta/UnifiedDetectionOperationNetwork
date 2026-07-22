"""
packetRoutes.py
----------------
Connects the PacketSniffer backend engine with REST endpoints.
Provides APIs to start, stop, retrieve, and reset live packet capture sessions.
"""

import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from app.capture.packetSniffer import PacketSniffer

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def verify_api_key(api_key: str = Depends(api_key_header)):
    expected_api_key = os.getenv("API_KEY", "default-secret-key")
    if api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key

# Initialize router and packet sniffer instance
router = APIRouter(dependencies=[Depends(verify_api_key)])
sniffer = PacketSniffer()


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@router.post("/start")
async def startPacketCapture():
    """
    Starts the sequential packet capture thread.
    """
    if sniffer.isCapturing:
        return {"status": "already_running", "detail": "Packet capture session is already active."}

    sniffer.startCapture()
    return {"status": "started", "detail": "Packet capture initiated successfully."}


@router.post("/stop")
async def stopPacketCapture():
    """
    Stops the currently active packet capture session.
    """
    if not sniffer.isCapturing:
        return {"status": "not_running", "detail": "No active capture session found."}

    sniffer.stopCapture()
    return {"status": "stopped", "detail": "Packet capture stopped successfully."}


@router.get("/latest")
async def getLatestPackets(limit: int = 50):
    """
    Retrieves the most recent packets captured by the sniffer.
    """
    packets = sniffer.getCapturedPackets(limit=limit)
    return {"count": len(packets), "packets": packets}


@router.delete("/reset")
async def resetSession():
    """
    Resets all sniffer state, clears captured data, and restarts packet ID sequence.
    """
    sniffer.resetCapture()
    return {"status": "reset", "detail": "Capture session and ID counter cleared."}


@router.get("/status")
async def getStatus():
    """
    Returns the current operational status of the packet sniffer.
    """
    return {
        "isCapturing": sniffer.isCapturing,
        "totalCaptured": len(sniffer.capturedPackets)
    }
