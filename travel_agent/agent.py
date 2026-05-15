import os
import asyncio
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

instruction_text = """
"Kamu adalah Travel AI Agent yang ramah dan profesional. "
            "Tugasmu adalah membantu pengguna mencari dan memesan hotel. "
            "Gunakan alat yang tersedia (search_hotels, book_hotel) untuk memeriksa database sungguhan. "
            "Jangan pernah mengarang ID hotel atau status ketersediaan. "
            "Selalu berikan informasi ID hotel saat memberikan daftar agar pengguna bisa memesannya."
"""

# Mendefinisikan Root Agent yang menggunakan model Gemini dan terkoneksi ke FastMCP Server kita
root_agent = LlmAgent(
    model='gemini-3-flash-preview',
    name="agent_travel",
    instruction= instruction_text,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp")
            )
        )
    ],
)