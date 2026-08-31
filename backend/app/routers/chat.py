# app/routers/chat.py
#
# PURPOSE: HTTP endpoint for the AI-powered conversational property search.
# Receives user messages, passes them to ChatService, returns AI response.
#
# PATTERN: Router layer — HTTP only. No business logic here.
# All AI logic lives in ChatService.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from pydantic import BaseModel
from app.database import get_db
from app.services.chat_service import ChatService

# ── Router setup ─────────────────────────────────────────────
# prefix="/api/chat" means all routes here start with /api/chat
router = APIRouter(prefix="/api/chat", tags=["chat"])

# ── Request schema ───────────────────────────────────────────
# Pydantic model for the incoming request body
class ChatRequest(BaseModel):
    message: str #The user's natural language message to the AI

# ── Response schema ──────────────────────────────────────────
class ChatResponse(BaseModel):
    response: str #The AI-generated response to the user's message
    properties_found: int #Number of properties found in the search
    properties: list #List of property details (could be empty if none found)

# ── POST /api/chat/ ──────────────────────────────────────────
# Recieve a user message, pass it to ChatService, return the AI response
#@router.post("/", response_model=ChatResponse)


