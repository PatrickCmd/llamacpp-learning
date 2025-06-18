# LLaMaCPP (LLaMaC++)

- [LLamaC++](https://github.com/ggml-org/llama.cpp)
- [LLaMaC++ - Server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [Youtube](https://www.youtube.com/watch?v=G_Raw7GEN0I)

## Installation with brew

```sh
brew install llama.cpp
```

### Serve quantized Phi-3 model

```sh
llama-server \
 --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \
 --hf-file Phi-3-mini-4k-instruct-q4.gguf
```

### Make Requests

#### 1. Curl

```sh
curl --request POST \
    --url http://localhost:8080/completion \
    --header "Content-Type: application/json" \
    --data '{"prompt": "Building a website can be done in 10 simple steps: ", "n_predict": 128 }' \
    | python -m json.tool
```

#### OpenAI Client

```python
import openai
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",  # "http://<Your api-server>:port"
    api_key="sk-no-key-required"
)

response = client.chat.completions.create(
    model="microsoft/Phi-3-mini-4k-instruct-gguf",
    messages=[
        {
            "role": "user",
            "content": "Building a website can be done in 10 simple steps: "
        }
    ],
)
print(response)
```

#### Requests Package

```python
import requests
import concurrent.futures

# Define the API endpoint and headers
url = "http://localhost:8080/v1/chat/completion"
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
print(response.json())
print(response.json()["choices"][0]["message"]["content"])
```
