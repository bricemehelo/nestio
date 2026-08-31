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


