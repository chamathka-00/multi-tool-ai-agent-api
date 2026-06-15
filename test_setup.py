from langchain_groq import ChatGroq

# Create a ChatGroq instance using the free Llama 3.3 70B model
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Send a test message to verify the connection
response = llm.invoke("Say hello in one sentence.")
print(response.content)