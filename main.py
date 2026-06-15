import uuid
from fastapi import FastAPI, HTTPException
from schemas import AgentQuery, AgentResponse
from agent import run_agent
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(
    title="AI Agent API",
    description="A multi-tool AI agent powered by LangChain and Groq",
    version="1.0.0",
)

# In-memory storage for conversation sessions
sessions: dict[str, list] = {}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/agent/query", response_model=AgentResponse)
async def query_agent(request: AgentQuery):
    # Generate a session ID if the client didn't provide one
    session_id = request.session_id or str(uuid.uuid4())
    message_history = sessions.get(session_id, [])

    try:
        result = await run_agent(query=request.query, message_history=message_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    # Save conversation history for this session
    sessions[session_id] = message_history + [
        HumanMessage(content=request.query),
        AIMessage(content=result["answer"]),
    ]

    return AgentResponse(
        answer=result["answer"],
        tools_used=result["tools_used"],
        model="llama-3.3-70b-versatile",
        session_id=session_id,
    )

@app.delete("/agent/sessions/{session_id}")
async def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "session cleared"}
    raise HTTPException(status_code=404, detail="Session not found")