"""Minimal AI-related endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Prompt(BaseModel):
    """Request model containing the user's prompt."""

    prompt: str


class MCPReply(BaseModel):
    """Mock response in the style of the Master Control Program."""

    response: str

@router.get("/")
async def ai_root():
    return {"message": "AI placeholder"}


@router.post("/mcp", response_model=MCPReply)
async def mcp_reply(prompt: Prompt) -> MCPReply:
    """Return a mocked MCP-style response for the given prompt."""

    text = prompt.prompt.strip()
    if not text:
        text = "..."
    # Placeholder logic - eventually this will call an external AI service
    return MCPReply(response=f"MCP mock reply: {text}")
