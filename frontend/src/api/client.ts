// src/api/client.ts
//
// PURPOSE: Creates a typed Axios instance as the single HTTP client for the app.
// All API calls go through this client — base URL and headers configured once here.
//
// PATTERN: Adapter — wraps Axios behind a consistent interface so the rest of
// the app never imports Axios directly. If we swap HTTP clients later, only this file changes.

import axios from "axios";

// Base URL points to the FastAPI backend
// In development this is localhost:8000
// In production this will be the Railway URL via environment variable

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Create a typed Axios instance with the base URL and default headers

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
