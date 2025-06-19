from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="amazon.nova-micro-v1:0",
)


messages = [
    ("human", "What is an LLM?."),
]
ai_msg = llm.invoke(input=messages)
print(ai_msg.content)