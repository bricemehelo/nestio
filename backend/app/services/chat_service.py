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

# Configure Gemini with our API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ── Tool Definitions ──────────────────────────────────────────
# Tools are functions Gemini can call to get real data.
# We define what the tool does and what parameters it needs.
# Gemini reads these definitions and decides when to call them.

tools = [
    {
        "function_declarations": [
            {
                # Tool 1: Search our PostgreSQL database
                "name": "search_properties",
                "description": (
                    "Search the Nestio property database for listings in Nigerian cities. "
                    "Use this first before searching the web. "
                    "Returns matching properties with price, location, and details."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name e.g. Lagos, Port Harcourt, Abuja"
                        },
                        "property_type": {
                            "type": "string",
                            "description": "Type of property: apartment, house, land, commercial"
                        },
                        "max_price": {
                            "type": "number",
                            "description": "Maximum price in Naira"
                        },
                        "min_price": {
                            "type": "number",
                            "description": "Minimum price in Naira"
                        },
                        "status": {
                            "type": "string",
                            "description": "for_sale or for_rent"
                        },
                        "search": {
                            "type": "string",
                            "description": "Keyword search e.g. Lekki, Ikoyi, quiet, gated"
                        }
                    },
                    "required": []
                }
            },
            {
                # Tool 2: Save a web-found property to our DB as unverified
                "name": "save_unverified_property",
                "description": (
                    "Save a property found from web search into the Nestio database "
                    "as an unverified listing. Use this when web search finds a property "
                    "that doesn't exist in our database yet."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "price": {"type": "number"},
                        "address": {"type": "string"},
                        "city": {"type": "string"},
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                        "property_type": {"type": "string"},
                        "status": {"type": "string"},
                        "source_url": {"type": "string"},
                    },
                    "required": ["title", "price", "city", "property_type", "status"]
                }
            }
        ]
    }
]


class ChatService:
    """
    Handles AI-powered property search using Google Gemini.
    
    Flow:
    1. User sends a natural language message
    2. Gemini decides to call search_properties tool
    3. We execute the search against PostgreSQL
    4. If results are insufficient, Gemini calls save_unverified_property
    5. We save new listings and return a combined response
    """

     def __init__(self, db: Session):
        # Database session injected by FastAPI dependency injection
        self.db = db
        self.repo = PropertyRepository(db)
        
        # Initialise Gemini model with tool use enabled
        # gemini-1.5-flash is fast and free tier friendly
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            tools=tools,
            system_instruction=(
                "You are Nestio AI, a helpful property search assistant for Nigerian real estate. "
                "You help users find properties in Lagos, Port Harcourt, Abuja and other Nigerian cities. "
                "Always search the database first using search_properties. "
                "If you find fewer than 3 results, mention that data is limited "
                "and describe what properties you did find. "
                "Be conversational, helpful, and specific about Nigerian locations. "
                "Format prices in Naira (₦) with proper formatting e.g. ₦85,000,000. "
                "Always mention the neighbourhood, not just the city."
            )
        )

