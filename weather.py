import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text.strip()}."
    except Exception as e:
        return f"Error: {e}"
    return "Something went wrong"
# Define the tool schema so the model knows the get_weather function exists
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city to get the weather for"}
                },
                "required": ["city"],
            },
        },
    }
]
user_query = input("> ")
messages = [{"role": "user", "content": user_query}]
# 1. Ask the model with the tool definition included
response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=messages,
    tools=tools,
)


print("harshit dhukla 1",response.choices[0].message.content)
response_message = response.choices[0].message
tool_calls = response_message.tool_calls
# 2. Check if the model decided to call the get_weather function
if tool_calls:
    # Append the assistant's request to call the tool
    messages.append(response_message)
    
    for tool_call in tool_calls:
        if tool_call.function.name == "get_weather":
            # Extract arguments and call the python function
            args = json.loads(tool_call.function.arguments)
            city_name = args.get("city")
            print(f"\n[Tool Execution] Running: get_weather(city='{city_name}')")
            
            weather_info = get_weather(city_name)
            print(f"[Tool Response] Result: {weather_info}")
            
            # Send the result of the function back to the model
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "get_weather",
                "content": weather_info,
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
    print("harshit shukla", response_message.content)
