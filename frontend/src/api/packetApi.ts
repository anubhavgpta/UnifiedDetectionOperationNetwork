// src/api/packetApi.ts
// This module defines all HTTP requests to the backend for packet operations.

const BASE_URL = "http://127.0.0.1:8000/api/packets";

/**
 * Initiates live packet capture on the backend.
 */
export async function startCapture(): Promise<any> {
  const response = await fetch(`${BASE_URL}/start`, { method: "POST" });
  if (!response.ok) throw new Error("Failed to start packet capture");
  return response.json();
}

/**
 * Stops the live packet capture process on the backend.
 */
export async function stopCapture(): Promise<any> {
  const response = await fetch(`${BASE_URL}/stop`, { method: "POST" });
  if (!response.ok) throw new Error("Failed to stop packet capture");
  return response.json();
}

/**
 * Retrieves the latest packets captured from the backend memory.
 */
export async function getLatestPackets(): Promise<any[]> {
  const response = await fetch(`${BASE_URL}/latest`);
  if (!response.ok) throw new Error("Failed to fetch packets");
  return response.json();
}

/**
 * Resets all captured data and clears the backend memory.
 */
export async function resetCapture(): Promise<any> {
  const response = await fetch(`${BASE_URL}/reset`, { method: "DELETE" });
  if (!response.ok) throw new Error("Failed to reset packet capture");
  return response.json();
}
