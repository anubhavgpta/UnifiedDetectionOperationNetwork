"""
packetRoutes.py
----------------
Connects the PacketSniffer backend engine with REST endpoints.
Provides APIs to start, stop, retrieve, and reset live packet capture sessions.
"""

from fastapi import APIRouter
from app.capture.packetSniffer import PacketSniffer

# Initialize router and packet sniffer instance
router = APIRouter()
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
