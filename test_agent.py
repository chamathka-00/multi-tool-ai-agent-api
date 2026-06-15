import asyncio
from agent import run_agent


async def main():
    # Test 1: Math query should call the calculate tool
    print("Test 1: Math query")
    result = await run_agent("What is 25 * 17 + 3?")
    print(f"Answer: {result['answer']}")
    print(f"Tools used: {result['tools_used']}")
    print()

    # Test 2: Text analysis should call the analyze_text tool
    print("Test 2: Text analysis")
    result = await run_agent("Analyze the text: Hello world")
    print(f"Answer: {result['answer']}")
    print(f"Tools used: {result['tools_used']}")


asyncio.run(main())