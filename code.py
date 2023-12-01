import json
import requests
import openai
from dotenv import load_dotenv
import os

#setting configurations
load_dotenv()
openai.api_type="azure"
openai.api_key=os.getenv('oai_key')
openai.api_base=os.getenv('oai_base')
openai.api_version ="2023-09-15-preview"


functions=[
        {
            "name":"getWeather",
            "description":"Retrieve real-time weather information/data about a particular location/place",
            "parameters":{
                "type":"object",
                "properties":{
                    "location":{
                        "type":"string",
                        "description":"the exact location whose real-time weather is to be determined",
                    },
                    
                },
                "required":["location"]
            },
        }
    ] 



messages=[
    {"role":"system", "content":"you are an assistant that helps people retrieve real-time weather data/info"},
    {"role":"user", "content":"how is the weather in Mumbai?"}
    
]

initial_response=openai.ChatCompletion.create(
    engine="newTestingModel",
    messages=messages,
    functions=functions,
    max_tokens=120,
    function_call="auto",
    api_version="2023-09-15-preview"
)

response_message=initial_response["choices"][0]["message"]
function_name=response_message["function_call"]["name"]


function_args=json.loads(response_message["function_call"]["arguments"])

for key in function_args:
    location = function_args[key]
    
#calling open weather map API for information retrieval
#fetching latitude and longitude of the specific location respectively
url = "http://api.openweathermap.org/geo/1.0/direct?q=" + location + "&limit=1&appid=3359253df8893c703afe90ef4ff31cf0"
response=requests.get(url)
get_response=response.json()
latitude=get_response[0]['lat']
longitude = get_response[0]['lon']

url_final = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=3359253df8893c703afe90ef4ff31cf0"
final_response = requests.get(url_final)
final_response_json = final_response.json()
weather=final_response_json['weather'][0]['description']
print(weather)
    

