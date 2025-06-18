import requests

# Define the API endpoint and headers
url = "http://localhost:8080/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer no-key"
}
messages = [{
    "role": "user",
    "content": "Building a website can be done in 10 simple steps: "
}]

data = {"messages": messages}
response = requests.post(url, headers=headers, json=data)
print(response.json()["choices"][0]["message"]["content"])