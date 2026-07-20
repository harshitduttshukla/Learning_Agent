from Agenets.wekipedia_agent import search_wikipedia
from Agenets.current_date import get_current_date
from Agenets.weather_agent import get_weather

TOOLS = {
    "search_wikipedia": {
        "fn": search_wikipedia,
        "desc": "search_wikipedia(query: str) — Search Wikipedia. Use simple topic names like 'France' or 'Albert Einstein'.",
        "schema": {
            "type": "function",
            "function": {
                "name": "search_wikipedia",
                "description": "Search Wikipedia. Use simple topic names like 'France' or 'Albert Einstein'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The query to search Wikipedia for"}
                    },
                    "required": ["query"],
                },
            },
        }
    },
    
    "get_current_date": {
        "fn": get_current_date,
        "desc": "get_current_date() — Get today's date and time. Pass empty JSON: {}",
        "schema": {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Get today's date and time. Pass empty JSON: {}",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }
    },

    "get_weather": {
        "fn": get_weather,
        "desc": "get_weather(city: str) — Get the current weather for a given city.",
        "schema": {
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
    }
}

def get_tools_schemas(tool_names=None):
    """
    Returns the list of tool schemas for OpenAI function calling.
    If tool_names is provided, returns schemas only for those tools.
    """
    if tool_names is None:
        tool_names = list(TOOLS.keys())
    return [TOOLS[name]["schema"] for name in tool_names if name in TOOLS and "schema" in TOOLS[name]]

def call_tool(tool_name, args=None):
    """
    Call a registered tool by name, passing the provided arguments.
    """
    if tool_name not in TOOLS:
        return f"Error: Tool '{tool_name}' not found in registry."
        
    fn = TOOLS[tool_name]["fn"]
    try:
        if args is None:
            return fn()
        elif isinstance(args, dict):
            return fn(**args)
        else:
            return fn(args)
    except Exception as e:
        return f"Error executing tool '{tool_name}': {e}"