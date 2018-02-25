import json

# variables pre-defined. In real life, these will be dynamically set. Note: this is based on what
# is in the Project 2 instructions

integer_milliseconds_since_epoc = 1464380051230
float_temperature_in_degrees_C = 27.0
# Note: can't have the percent symbol as part of a variable name
float_humidity_percent = 36.0

#############################################################################################
# json as pure string. Note: This is a cut and paste of what is in our Project 2 instructions

# Note: I need to use triple quotes as it is a multi-line string

pure_string_json = """{
 "timestamp": integer_milliseconds_since_epoc,
 "data": {
 "temperature": float_temperature_in_degrees_C,
 "humidity": float_humidity_percent
 }
}
"""

print(pure_string_json) 


#############################################################################################
# json as a python dictionary

json_dict = {}
json_dict["timestamp"] = integer_milliseconds_since_epoc

json_data_dict = {}
json_data_dict["temperature"] = float_temperature_in_degrees_C
json_data_dict["humidity"] = float_humidity_percent

json_dict["data"] = json_data_dict

print(json_dict) 

#############################################################################################
# converting python dictionary to a proper json string using the json library

json_proper = json.dumps(json_dict)

print(json_proper)
