import json

data = {
    "name": "John",
    "age": 25,
    "city": "New York"
}

json_string = json.dumps(data)
print(json_string)
print(json.loads(json_string))


