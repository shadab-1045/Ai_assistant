#structure for tool calling: 

# "type": "function",
# "function": {
#     "name": "function_name",
#     "description": "Function description like what it does and how to use it",
#     "parameters": {....}
# }


# format for parameters:
# parameters": {
#     "type": "object",
#     "properties": {
#         "param1": {
#             "type": "string",
#             "enum": ["value1", "value2", "value3"], // optional, if you want to restrict the values
#             "description": "Description of param1"
#         },
#         "param2": {
#             "type": "integer",
#             "description": "Description of param2"
#         },
#         "param3": {
#             "type": "array",
#             "items": {
#                 "type": "string"
#             },
#             "description": "Description of param3"
#         }
#     },
#     "required": ["param1"] // list of required parameters
# }
import json

import requests
from datetime import datetime
from urllib.parse import quote

from Utilities.utilities import log


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_weather(city:str):
    url = f"https://wttr.in/{quote(city, safe='')}?format=4"
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

def my_city():
    return "pune"



def run_tool(tool_call):
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


#TOOLS
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
