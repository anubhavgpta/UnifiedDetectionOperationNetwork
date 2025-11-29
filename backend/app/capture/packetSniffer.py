"""
packetSniffer.py
----------------
Implements sequential packet capture using Scapy.
This module ensures that each packet is processed in order without skipping,
assigning continuous incremental IDs and storing minimal metadata for analysis.
"""

from scapy.all import sniff, Packet
from datetime import datetime
from app.utils.idGenerator import PacketIDGenerator
from app.utils.logger import SystemLogger
from app.capture.packetParser import parsePacket
from typing import List, Dict
import threading


class PacketSniffer:
    """
    Handles live packet sniffing in a separate thread.
    Provides start, stop, and retrieval operations for sequential packets.
    """

    def __init__(self):
        # Sequential ID generator to maintain continuous packet IDs
        self.idGenerator = PacketIDGenerator()
        # Thread-safe list to store captured packet metadata
        self.capturedPackets: List[Dict] = []
        # Internal flag to control capture session state
        self.isCapturing: bool = False
        # Thread handle for live capture
        self.captureThread = None
        # Logger instance for system-level events
        self.logger = SystemLogger("packet_sniffer")

    # -----------------------------------------------------------------------
    # Internal Capture Handler
    # -----------------------------------------------------------------------

    def _processPacket(self, packet: Packet) -> None:
        """
        Callback executed for every packet captured by Scapy.
        Extracts metadata, assigns a sequential ID, and stores it.
        """
        packetId = self.idGenerator.getNextId()
        parsedData = parsePacket(packet, packetId)
        self.capturedPackets.append(parsedData)
        self.logger.logInfo(f"Captured Packet #{packetId}: {parsedData['protocol']}")

    def _captureLoop(self, iface: str = None) -> None:
        """
        Runs the packet sniffing loop in a background thread.
        The 'store=False' parameter prevents Scapy from keeping packet objects in memory.
        """
        self.logger.logInfo("Packet capture loop initiated.")
        try:
            sniff(
                prn=self._processPacket,  # Callback per packet
                store=False,              # Avoid memory growth
                stop_filter=lambda x: not self.isCapturing,
                iface=iface               # Interface to sniff from
            )
        except Exception as e:
            self.logger.logError(f"Error during packet capture: {str(e)}")

    # -----------------------------------------------------------------------
    # Public Methods
    # -----------------------------------------------------------------------

    def startCapture(self, iface: str = None) -> None:
        """
        Initiates the packet capture process in a separate thread.
        """
        if self.isCapturing:
            self.logger.logWarning("Attempted to start capture, but a session is already active.")
            return

        self.isCapturing = True
        self.capturedPackets.clear()
        self.logger.logInfo("Starting live packet capture...")

        self.captureThread = threading.Thread(target=self._captureLoop, args=(iface,), daemon=True)
        self.captureThread.start()

    def stopCapture(self) -> None:
        """
        Stops the ongoing packet capture session safely.
        """
        if not self.isCapturing:
            self.logger.logWarning("Attempted to stop capture, but no session is active.")
            return

        self.isCapturing = False
        self.logger.logInfo("Stopping live packet capture...")
        if self.captureThread and self.captureThread.is_alive():
            self.captureThread.join(timeout=2.0)

    def getCapturedPackets(self, limit: int = 50) -> List[Dict]:
        """
        Returns the most recently captured packets up to the specified limit.
        This data will be delivered to the frontend for visualization.
        """
        return self.capturedPackets[-limit:]

    def resetCapture(self) -> None:
        """
        Resets the internal state of the sniffer, clearing all captured data and IDs.
        """
        self.stopCapture()
        self.capturedPackets.clear()
        self.idGenerator.reset()
        self.logger.logInfo("Capture session reset successfully.")
