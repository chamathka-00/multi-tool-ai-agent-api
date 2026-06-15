import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from tools import calculate, analyze_text, get_current_datetime


def get_agent():
    # Initialize the Groq LLM with Llama 3.3 70B
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    # Create a LangChain agent with our three tools
    agent = create_agent(llm, tools=[calculate, analyze_text, get_current_datetime])
    return agent

async def run_agent(query: str, message_history: list | None = None) -> dict:
    agent = get_agent()
    messages = []
    # Prepend any existing conversation history
    if message_history:
        messages.extend(message_history)
    # Add the current user query
    messages.append(HumanMessage(content=query))

    # Invoke the agent asynchronously
    response = await agent.ainvoke({"messages": messages})

    # Extract the final answer from the last message
    agent_messages = response["messages"]
    final_message = agent_messages[-1]

    # Collect names of any tools the agent called
    tools_used = []
    for msg in agent_messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tools_used.append(tool_call["name"])

    return {
        "answer": final_message.content,
        "tools_used": tools_used,
        "all_messages": agent_messages,
    }

