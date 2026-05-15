# mcp-travel-agent-use-google-adk

This project is an AI Travel Agent implementation designed to help users search for and book hotels. It leverages the **Google ADK (Agent Development Kit)** with a Gemini model for user interaction and **FastMCP (Fast Multi-Agent Communication Protocol)** to manage backend operations and database tools.

## Features

*   **Hotel Search:** Users can search for available hotels in specific locations. The agent returns detailed information including Hotel ID, name, price tier, and availability dates.
*   **Hotel Booking:** Users can book a hotel using its unique ID. The agent validates availability in the real-time database and updates the booking status upon success.

## Technical Architecture

The project consists of two primary components:

1.  **MCP Server (`server.py`):**
    *   Manages a SQLite database (`travel.db`) storing hotel data.
    *   Exposes two tools via FastMCP: `search_hotels` and `book_hotel`.
    *   Handles data persistence and availability logic.

2.  **Travel Agent (`agent.py`):**
    *   An AI agent built using the `LlmAgent` class from Google ADK.
    *   Utilizes the `gemini-3-flash-preview` model.
    *   Connects to the backend through `McpToolset` to execute database-driven tasks.

## Getting Started

1.  **Initialize Database & Start Server:**
    Run `python mcp_server/server.py` to set up the SQLite database and start the MCP server on `http://localhost:9000`.
2.  **Run the Agent:**
    Interact with the agent via `travel_agent/agent.py` to start searching and booking hotels through natural language.