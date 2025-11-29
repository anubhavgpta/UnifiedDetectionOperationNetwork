"""
idGenerator.py
---------------
Provides a thread-safe mechanism for generating strictly sequential packet IDs.
This ensures that no packets are skipped or misnumbered during live capture.
"""

import threading


class PacketIDGenerator:
    """
    Generates monotonically increasing packet IDs across capture sessions.
    Thread-safe to avoid race conditions when multiple packets arrive rapidly.
    """

    def __init__(self):
        # Internal counter for packet IDs
        self.currentId: int = 0
        # Lock ensures atomic increments
        self.lock = threading.Lock()

    def getNextId(self) -> int:
        """
        Returns the next sequential packet ID in a thread-safe manner.
        """
        with self.lock:
            self.currentId += 1
            return self.currentId

    def reset(self) -> None:
        """
        Resets the packet ID counter to zero.
        Used when restarting a capture session.
        """
        with self.lock:
            self.currentId = 0
