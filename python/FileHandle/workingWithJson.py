import fileHandling
import json
import os.path
# Take a JSON string representing a person (name, age, city),
# convert it to a dictionary with json.loads(), and print each field.

print(fileHandling.project_root_path)

user_details = '{"name": "Santhosh", "age": "28", "city": "Bengaluru"}'
user_details_to_json = json.loads(user_details)
print(user_details_to_json["name"])
print(user_details_to_json["age"])
print(user_details_to_json.get("city", "CITY key not found"))

# Take a Python dictionary you create yourself,
# convert it to JSON text with json.dumps(..., indent=4), and print it.
user_deatils_in_dict = {"name": "Santhosh", "age": "28", "city": "Bengaluru"}
stringFormat = json.dumps(user_deatils_in_dict) #indent for space from line start
print(stringFormat)

# Write a Python dictionary to a .json file using json.dump().
# Then read that same file back using json.load() and print its contents.
dirname = os.path.dirname(os.path.abspath(__file__))
project_root_path = os.path.join(dirname, "..", "..", "..", "Test_Data")
print(project_root_path)
os.makedirs(project_root_path, exist_ok=True) #mode is to give permission the folder
with open(f'{project_root_path}\\string_to_json.json', "w") as file:
    json.dump(user_deatils_in_dict, file, indent=4)

with open(f'{project_root_path}\\string_to_json.json', "r") as file:
    reader = json.load(file)
    for key, value in reader.items():
        print(f'{key}: {value}')

# Create a nested JSON string (like the user/roles example above)
# and practice digging into it — access a value 2 levels deep, and one inside a nested list.
api_response_text = '''
{
    "status_code": 200,
    "endpoint": "/users/1",
    "body": {
        "id": 1,
        "name": "Alex",
        "email": ["alex@test.com", "sk@gmail.com"]
    },
    "response_time_ms": 145
}
'''
api_response_text_in_dict = json.loads(api_response_text)
print(api_response_text_in_dict["status_code"])
print(api_response_text_in_dict["endpoint"])
print(api_response_text_in_dict["body"]["id"])
print(api_response_text_in_dict.get("body").get("id"))
print(api_response_text_in_dict.get("body").get("email")[1])

# Print the status code using .get()
# If status_code is not 200, print the nested error message from inside "body" — use chained .get() with a default this time
# Print a default message using .get() if "response_time_ms" doesn't exist in the dictionary
# Bonus: convert this whole dictionary to a JSON string with json.dumps(), pretty-printed
api_response = {
    "status_code": 404,
    "endpoint": "/users/99",
    "body": {
        "error": "User not found"
    }
}
print(api_response.get("status_code"))
if api_response.get("status_code") != 200:
    print(api_response.get("body", {}).get("error"))

print(api_response.get("response_time_ms", "Response_time is not in the response"))
print(json.dumps(api_response, indent=4))
