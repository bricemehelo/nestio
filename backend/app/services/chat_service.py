# app/services/chat_service.py
#
# PURPOSE: Handles the AI-powered conversational property search.
# Uses Google Gemini with tool use to:
# 1. Search our PostgreSQL database for matching properties
# 2. Fall back to web search if DB results are insufficient
# 3. Auto-save web-found properties as unverified listings
#
# PATTERN: Service layer — business logic only, no HTTP concerns.
# The router calls this service, this service calls the repository.

import os
import json
import google.generativeai as genai
from sqlalchemy.orm import Session
from app.repositories.property_repo import PropertyRepository
from app.models.property import Property
from datetime import datetime

# Configure Gemini with our API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ── Tool Definitions ──────────────────────────────────────────
# Tools are functions Gemini can call to get real data.
# We define what the tool does and what parameters it needs.
# Gemini reads these definitions and decides when to call them.

