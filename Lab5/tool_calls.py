import json
import requests
from openai import OpenAI

# Initialize the OpenAI client pointing to local Ollama
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def get_weather(location):
    """Fetches current weather for a given location using Open-Meteo."""
    try:
        # First, get coordinates for the location
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url).json()
        
        if not geo_response.get("results"):
            return f"Could not find coordinates for {location}."
            
        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        
        # Then, get the weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
        weather_response = requests.get(weather_url).json()
        
        temp = weather_response["current"]["temperature_2m"]
        return f"The current temperature in {location} is {temp} degrees Celsius."
    except Exception as e:
        return f"Error fetching weather: {e}"

# Define the tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specified location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. Timisoara, Bucharest",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

def run_plain_model(user_input):
    """Runs the model without any tools."""
    response = client.chat.completions.create(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def run_tool_model(user_input):
    """Runs the model with the weather tool."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided tools when needed."},
        {"role": "user", "content": user_input}
    ]
    
    response = client.chat.completions.create(
        model="mistral",
        messages=messages,
        tools=tools
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            if tool_call.function.name == "get_weather":
                args = json.loads(tool_call.function.arguments)
                result = get_weather(args["location"])
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
                
        # Second call to get the final answer based on the tool's result
        final_response = client.chat.completions.create(
            model="mistral",
            messages=messages,
            tools=tools
        )
        return final_response.choices[0].message.content
    else:
         return msg.content

if __name__ == "__main__":
    print("=== Sistem de Comparare: Plain vs Tool-Enabled ===")
    print("(Scrie 'exit' pentru a termina)\n")
    
    while True:
        user_input = input("Tu: ")
        if user_input.lower() == 'exit':
            break
            
        print("\n[MODEL PLAIN]: ", run_plain_model(user_input))
        print("[MODEL CU TOOLS]: ", run_tool_model(user_input))
        print("\n")