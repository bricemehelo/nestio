# app/services/chat_service.py
#
# PURPOSE: Handles the AI-powered conversational property search.
# Uses Google Gemini with tool use to:
# 1. Search our PostgreSQL database for matching properties
# 2. Fall back to web search if DB results are insufficient
# 3. Let Gemini identify useful web-found properties
# 4. Save those web-found properties as unverified listings
#
# FLOW:
# Database search → Web search (if needed) → Save web properties → Final response
#
# PATTERN: Service layer — business logic only, no HTTP concerns.
# The router calls this service, this service calls the repository.

import os
import json
from google import genai
from google.genai import types
from sqlalchemy.orm import Session
from app.repositories.property_repo import PropertyRepository
from app.models.property import Property
from datetime import datetime
from googleapiclient.discovery import build

# ← ADD THIS LINE HERE — top level, no indentation
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ── Tool Definitions ──────────────────────────────────────────
# Tools are functions Gemini can call to get real data.
# We define what the tool does and what parameters it needs.
# Gemini reads these definitions and decides when to call them.

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_properties",
                description=(
                    "Search the Nestio property database for listings in Nigerian cities. "
                    "Always use this tool first before searching the web. "
                    "Returns matching properties with price, location, and details."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "city": types.Schema(
                            type=types.Type.STRING,
                            description="City name e.g. Lagos, Port Harcourt, Abuja"
                        ),
                        "property_type": types.Schema(
                            type=types.Type.STRING,
                            description="Type: apartment, house, land, commercial"
                        ),
                        "max_price": types.Schema(
                            type=types.Type.NUMBER,
                            description="Maximum price in Naira"
                        ),
                        "min_price": types.Schema(
                            type=types.Type.NUMBER,
                            description="Minimum price in Naira"
                        ),
                        "status": types.Schema(
                            type=types.Type.STRING,
                            description="for_sale or for_rent"
                        ),
                        "search": types.Schema(
                            type=types.Type.STRING,
                            description="Keyword search e.g. Lekki, Ikoyi, quiet, gated"
                        ),
                    },
                    required=[]
                )
            ),
            types.FunctionDeclaration(
                name="search_web",
                description=(
                    "Search Nigerian property websites when the database has fewer than 3 results. "
                    "Searches PropertyPro, Nigeria Property Centre, Jiji and other Nigerian property sites."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="Search query e.g. '3 bedroom apartment Lekki Lagos for rent'"
                        )
                    },
                    required=["query"]
                )
            ),
            types.FunctionDeclaration(
                name="save_unverified_property",
                description=(
                    "Save a property found from web search into the Nestio database "
                    "as an unverified listing. Use this after search_web finds relevant properties."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "title": types.Schema(type=types.Type.STRING),
                        "description": types.Schema(type=types.Type.STRING),
                        "price": types.Schema(type=types.Type.NUMBER),
                        "address": types.Schema(type=types.Type.STRING),
                        "city": types.Schema(type=types.Type.STRING),
                        "latitude": types.Schema(type=types.Type.NUMBER),
                        "longitude": types.Schema(type=types.Type.NUMBER),
                        "property_type": types.Schema(type=types.Type.STRING),
                        "status": types.Schema(type=types.Type.STRING),
                        "source_url": types.Schema(type=types.Type.STRING),
                    },
                    required=["title", "price", "city", "property_type", "status"]
                )
            ),
        ]
    )
]

class ChatService:
    """
    Handles AI-powered property search using Google Gemini.
    
    Flow:
    1. User sends a natural language message
    2. Gemini calls search_properties to search PostgreSQL
    3. We execute the database search and return results to Gemini
    4. If fewer than 3 results are found, Gemini calls search_web
    5. We execute the web search and return the results to Gemini
    6. Gemini identifies relevant web properties and calls save_unverified_property
    7. We save those properties as unverified listings
    8. Gemini generates the final response
    """

    def __init__(self, db: Session):
        # Database session injected by FastAPI dependency injection
        self.db = db
        self.repo = PropertyRepository(db)
        
        # Initialise Gemini model with tool use enabled
        # gemini-1.5-flash is fast and free tier friendly
        

    def _search_web(self, query: str) -> list:
        """
        Search Nigerian property sites using Google Custom Search API.
        Returns a list of raw search results for Gemini to process.
        
        Args:
            query: Search query e.g. "3 bedroom apartment Lekki Lagos for rent"
            
        Returns:
            List of search results with title, link, and snippet
        """

        try:
            # Build the Google Custom Search service
            service = build(
                "customsearch",
                "v1",
                developerKey=os.getenv("GOOGLE_SEARCH_API_KEY")
            )

            # Execute the search against our Nigerian property sites
            results = service.cse().list(
                q=query,
                cx=os.getenv("GOOGLE_SEARCH_ENGINE_ID"),
                num=5  # Return top 5 results
            ).execute()

            # Extract relevant fields from results
            items = results.get("items", [])
            formatted = []
            for item in items:
                formatted.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                })

            return formatted
        
        except Exception as e:
            print(f"Web search error: {e}")
        return []

    def _execute_search_properties(self, args: dict) -> str:
        """
        Execute the search_properties tool call against PostgreSQL.
        Returns results as a JSON string for Gemini to read.
        """
        # Call our existing repository with the args Gemini extracted
        results = self.repo.get_all(
            city=args.get("city"),
            property_type=args.get("property_type"),
            status=args.get("status"),
            search=args.get("search"),
            min_price=args.get("min_price"),
            max_price=args.get("max_price"),
            skip=0,
            limit=10
        )

        properties = results["properties"]

        if not properties:
            return json.dumps({
                "found": 0,
                "message": "No properties found in database matching these criteria.",
                "properties": []
            })

        # Format properties for Gemini to read
        formatted = []
        for p in properties:
            formatted.append({
                "id": p.id,
                "title": p.title,
                "price": float(p.price),
                "address": p.address,
                "city": p.city,
                "property_type": p.property_type,
                "status": p.status,
                "verified": p.verified,
                "description": p.description[:200] if p.description else ""
            })

        return json.dumps({
            "found": len(formatted),
            "properties": formatted
        })

    def _execute_save_unverified_property(self, args: dict) -> str:
        """
        Execute the save_unverified_property tool call.
        Saves a web-found property to our DB as unverified.
        """
        try:
            # Create new property marked as unverified and sourced from web search
            new_property = Property(
                title=args.get("title", "Untitled Property"),
                description=args.get("description", ""),
                price=args.get("price", 0),
                address=args.get("address", ""),
                city=args.get("city", ""),
                # Default coordinates for Lagos if not provided
                latitude=args.get("latitude", 6.5244),
                longitude=args.get("longitude", 3.3792),
                property_type=args.get("property_type", "apartment"),
                status=args.get("status", "for_sale"),
                # Verification fields — unverified by default
                source_url=args.get("source_url", ""),
                source="web_search",
                verified=False,
                verification_count=0,
                outdated_count=0,
            )

            self.db.add(new_property)
            self.db.commit()
            self.db.refresh(new_property)

            return json.dumps({
                "saved": True,
                "property_id": new_property.id,
                "message": f"Saved '{new_property.title}' as unverified listing."
            })

        except Exception as e:
            self.db.rollback()
            return json.dumps({"saved": False, "error": str(e)})
        
    def chat(self, message: str) -> dict:
        """
        Process a user message and return AI response.

        Args:
            message: Natural language property search query

        Returns:
            dict with response text and found properties
        """
        system_instruction = (
            "You are Nestio AI, a helpful property search assistant for Nigerian real estate. "
            "You help users find properties in Lagos, Port Harcourt, Abuja and other Nigerian cities. "
            "Always search the database first using search_properties. "
            "If fewer than 3 results are found, use search_web to find more properties online. "
            "For any relevant web results, call save_unverified_property to save them. "
            "Be conversational and specific about Nigerian locations. "
            "Format prices in Naira (₦) e.g. ₦85,000,000."
        )

        # Build conversation history
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
        ]

        found_properties = []
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Send message to Gemini
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=tools,
                )
            )

            # Add Gemini's response to conversation history
            contents.append(
                types.Content(
                    role="model",
                    parts=response.candidates[0].content.parts
                )
            )

            # Check if Gemini wants to call any tools
            tool_calls_made = False
            tool_results = []

            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    tool_calls_made = True
                    tool_name = part.function_call.name
                    tool_args = dict(part.function_call.args)

                    # Execute the requested tool
                    if tool_name == "search_properties":
                        tool_result = self._execute_search_properties(tool_args)
                        result_data = json.loads(tool_result)
                        if result_data.get("properties"):
                            found_properties.extend(result_data["properties"])

                    elif tool_name == "search_web":
                        tool_result = self._execute_search_web(
                            tool_args.get("query", "")
                        )

                    elif tool_name == "save_unverified_property":
                        tool_result = self._execute_save_unverified_property(tool_args)

                    else:
                        tool_result = json.dumps({"error": f"Unknown tool: {tool_name}"})

                    # Collect tool result
                    tool_results.append(
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=tool_name,
                                response={"result": tool_result}
                            )
                        )
                    )

            # Send all tool results back to Gemini in one message
            if tool_calls_made and tool_results:
                contents.append(
                    types.Content(
                        role="user",
                        parts=tool_results
                    )
                )
                continue

            # No tool calls — Gemini has finished, extract final text
            final_text = ""
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    final_text += part.text

            return {
                "response": final_text,
                "properties_found": len(found_properties),
                "properties": found_properties
            }

        return {
            "response": "I could not complete the search. Please try again.",
            "properties_found": 0,
            "properties": []
        }
    
        """
        Main entry point — process a user message and return AI response.
        
        Args:
            message: Natural language property search query from user
            
        Returns:
            dict with 'response' (AI text) and 'properties' (any found listings)
        """
        # Start a chat session with Gemini
        chat_session = self.model.start_chat()

        # Send user message to Gemini
        response = chat_session.send_message(message)

        # Track properties found during this conversation
        found_properties = []

        # ── Tool Use Loop ─────────────────────────────────────
        # Gemini may call multiple tools in sequence.
        # We loop until Gemini stops calling tools and gives a final text response.
        max_iterations = 5  # prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            tool_calls_made = False

            # Check if Gemini wants to call any tools
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call.name:
                        tool_calls_made = True
                        tool_name = part.function_call.name
                        tool_args = dict(part.function_call.args)

                        # Execute the tool Gemini requested
                        if tool_name == "search_properties":
                            tool_result = self._execute_search_properties(tool_args)
                            
                            # Track found properties for the frontend
                            result_data = json.loads(tool_result)
                            if result_data.get("properties"):
                                found_properties.extend(result_data["properties"])

                        elif tool_name == "save_unverified_property":
                            tool_result = self._execute_save_unverified_property(tool_args)

                        elif tool_name == "search_web":
                            # Execute real web search against Nigerian property sites
                            web_results = self._search_web(tool_args.get("query", ""))
                            tool_result = json.dumps({
                                "results_found": len(web_results),
                                "results": web_results,
                                "instruction": (
                                    "For each relevant result, call save_unverified_property "
                                    "to save it to the database before responding to the user."
                                )
                            })

                        else:
                            tool_result = json.dumps({"error": f"Unknown tool: {tool_name}"})

                        # Send tool result back to Gemini so it can continue
                        response = chat_session.send_message(
                            genai.protos.Content(
                                parts=[genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=tool_name,
                                        response={"result": tool_result}
                                    )
                                )],
                                role="user"
                            )
                        )

            # If no tool calls were made, Gemini has finished — extract text response
            if not tool_calls_made:
                final_text = ""
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text'):
                            final_text += part.text

                return {
                    "response": final_text,
                    "properties_found": len(found_properties),
                    "properties": found_properties
                }

        # Fallback if max iterations reached
        return {
            "response": "I searched for properties but couldn't complete the request. Please try again.",
            "properties_found": 0,
            "properties": []
        }