# app/main.py
# ─────────────────────────────────────────────────────────────
# This is the ENTRY POINT of the entire backend application.
# Uvicorn runs this file. It creates the FastAPI app instance,
# registers all middleware, and will connect all routers.
# Think of it as the front door of your backend.
# ─────────────────────────────────────────────────────────────

# FastAPI is the web framework — handles HTTP requests and responses
from fastapi import FastAPI

# CORSMiddleware allows our React frontend (on a different port)
# to make requests to this API without being blocked by the browser
from fastapi.middleware.cors import CORSMiddleware

# ── Create the FastAPI application instance ──────────────────
# This is the Singleton — one app instance shared everywhere.
# title, description, version appear in the auto-generated docs
# at http://localhost:8000/docs
app = FastAPI(
    title="Nestio FastAPI Backend",
    description="Property listings API built with FastAPI",
    version="1.0.0"
)

# ── Register CORS Middleware ──────────────────────────────────
# CORS (Cross-Origin Resource Sharing) is a browser security rule.
# By default browsers block requests from one origin (localhost:5173)
# to a different origin (localhost:8000).
# This middleware tells the browser: "React frontend is allowed."
app.add_middleware(
    CORSMiddleware,

    # The exact origin of our React frontend dev server
    # In production this will be replaced with your real domain
    allow_origins=["http://localhost:5173"],

    # Allows cookies and auth headers to be sent cross-origin
    allow_credentials=True,

    # Allow all HTTP methods — GET, POST, PUT, DELETE, PATCH etc.
    allow_methods=["*"],

    # Allow all headers — Content-Type, Authorization etc.
    allow_headers=["*"],
)

# ── Root route ───────────────────────────────────────────────
# A simple GET endpoint at the root URL: http://localhost:8000/
# Used to confirm the API is alive.
# The @app.get("/") is the Decorator pattern in action —
# it adds HTTP GET behaviour to the function below it
# without changing the function itself.
@app.get("/")
def root():
    # FastAPI automatically converts this dict to a JSON response
    return {"message": "Nestio API is running"}


# ── Health check route ───────────────────────────────────────
# Industry standard endpoint: http://localhost:8000/health
# Used by Docker, AWS, and monitoring tools to check if the
# service is alive. Returns 200 OK with a status message.
# You will see this in every production backend.
@app.get("/health")
def health():
    return {"status": "healthy"}

# ── Root route ───────────────────────────────────────────────
# A simple GET endpoint at the root URL: http://localhost:8000/
# Used to confirm the API is alive.
# The @app.get("/") is the Decorator pattern in action —
# it adds HTTP GET behaviour to the function below it
# without changing the function itself.
@app.get("/")
def root():
    # FastAPI automatically converts this dict to a JSON response
    return {"message": "Nestio API is running"}


# ── Health check route ───────────────────────────────────────
# Industry standard endpoint: http://localhost:8000/health
# Used by Docker, AWS, and monitoring tools to check if the
# service is alive. Returns 200 OK with a status message.
# You will see this in every production backend.
@app.get("/health")
def health():
    return {"status": "healthy"}
