from pydantic import BaseModel, Field


class AgentQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The question or task for the agent")
    session_id: str | None = Field(default=None, description="Optional session ID for conversation memory")

class AgentResponse(BaseModel):
    answer: str = Field(..., description="The agent's response")
    tools_used: list[str] = Field(default_factory=list, description="List of tools the agent called")
    model: str = Field(default="llama-3.3-70b-versatile", description="The LLM model used")
    session_id: str | None = Field(default=None, description="Session ID if conversation memory is active")