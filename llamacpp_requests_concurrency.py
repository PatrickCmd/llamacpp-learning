import requests
import concurrent.futures

# Define the API endpoint and headers
url = "http://localhost:8080/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer no-key"
}

# Create a list of user messages and populate it with sample questions requests
user_messages = [
    "What is the capital of France?",
    "How do I make a cake?",
    "What is the weather like today?",
    "Tell me a joke.",
    "What is the meaning of life?",
    "How do I learn Python?",
    "What is the best way to stay healthy?",
    "Can you recommend a good book?",
    "What is the latest news?",
    "How do I fix a flat tire?"
]

# Function to send a request to the API
def send_request(message):
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant"},
        {"role": "user", "content": message}
    ]
    
    data = {"messages": messages}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an error for bad responses
    
    return response.json()
    

# Main function to make concurrent API calls
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all requests to the executor
        future_to_message = {executor.submit(send_request, msg): msg for msg in user_messages}
        
        # Process the results as they complete
        for future in concurrent.futures.as_completed(future_to_message):
            message = future_to_message[future]
            try:
                result = future.result()
                print(f"Response for '{message}': {result['choices'][0]['message']['content']}")
            except Exception as e:
                print(f"Error processing message '{message}': {e}")


if __name__ == "__main__":
    main()
