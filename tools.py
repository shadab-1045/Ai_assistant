"""Define the assistant's callable tools and their local implementations."""

import json
import requests
from datetime import datetime
from urllib.parse import quote

from Utilities.utilities import log


def get_current_time():
    """Return the local date and time in a model-friendly format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_weather(city:str):
    """Fetch current weather for a city using wttr.in."""
    url = f"https://wttr.in/{quote(city, safe='')}?format=4"
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

def my_city():
    """Return the configured home city."""
    return "pune"



def run_tool(tool_call):
    """Dispatch a model-requested tool call and return its result as text."""
    func_name=tool_call.function.name
    func_params={}
            
    try:
        func_params=json.loads(tool_call.function.arguments or "{}")
        log(f"        function : {func_name} : {func_params}")
        fn = FUNCTION_NAME_FUNCTION_MAP.get(func_name)
        result = fn(**func_params)
    except Exception as e:
        result = f"Error occurred while calling {func_name}: {str(e)}"
                
    log(f"        result : {result}")
    return str(result)


# Schemas exposed to the model; keep their function names in sync with the map below.
TOOLS=[
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "returns the current date and time in the format YYYY-MM-DD HH:MM:SS",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description":"returns the current live weather for a given city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"The name of the city to get the weather for"
                    }
                },
                "required":["city"]
                
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"my_city",
            "description":"returns the name of my city where I am currently located",
            "parameters":{
                "type":"object",
                "properties":{},
                "required":[]
                
            }
        }
    }
]

FUNCTION_NAME_FUNCTION_MAP={
    "get_current_time": get_current_time,
    "get_weather": get_weather,
    "my_city": my_city
}
