import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tool_registry import get_tools_schemas, call_tool

# Load environment variables (such as OPENROUTER_API_KEY)
load_dotenv()

# Initialize the OpenAI client pointing to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def run_agent():
    # Retrieve all tools dynamically from the registry
    tools = get_tools_schemas()
    
    # Get user prompt
    user_query = input("> ")
    messages = [{"role": "user", "content": user_query}]
    
    # 1. Call the model with tool definitions included
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=messages,
        tools=tools,
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # 2. Check if the model decided to call any function(s)
    if tool_calls:
        # Append the assistant's request to call the tool
        messages.append(response_message)
        
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"\n[Tool Execution] Running: {tool_name}({args})")
            
            tool_response = call_tool(tool_name, args)
            print(f"[Tool Response] Result: {tool_response}")
            
            # Send the result of the function back to the model
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_name,
                "content": tool_response,
            })
            
        # 3. Call the model again with the tool output included
        second_response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages,
        )
        print("\n[AI Final Response]:")
        print(second_response.choices[0].message.content)
    else:
        # Direct response if no function call was needed
        print("\n[AI Final Response]:")
        print(response_message.content)

if __name__ == "__main__":
    run_agent()
