import requests

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text.strip()}."
    except Exception as e:
        return f"Error: {e}"
    return "Something went wrong"
