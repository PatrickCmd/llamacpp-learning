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
print(response.choices[0].message.content)