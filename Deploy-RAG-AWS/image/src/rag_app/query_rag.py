from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock

import sys, os

# Add parent src directory to PYTHONPATH for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from rag_app.get_chroma_db import get_chroma_db

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

BEDROCK_MODEL_ID = "anthropic.claude-3-5-haiku-20241022-v1:0"


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]


def query_rag(query_text: str) -> QueryResponse:
    db = get_chroma_db()
    # start with the default global model ID
    model_id = BEDROCK_MODEL_ID

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)
    print(f"Using model_id: {model_id}")

    try:
        model = ChatBedrock(model_id=model_id)
        response = model.invoke(prompt)
        response_text = response.content
    except Exception as e:
        print(f"Bedrock chat failed: {e}. Falling back to using amazon nova micro model.")
        model_id = "amazon.nova-micro-v1:0"
        model = ChatBedrock(model_id=model_id)
        response = model.invoke(prompt)
        response_text = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_text, response_text=response_text, sources=sources
    )


if __name__ == "__main__":
    # text = "How much does a landing page cost to develop?"
    # text = "What is the typical timeline for completing a website project?"
    # text = "What are some of the range of small businesses can benefit from Galaxy Design Agency services?"
    text = "How much does a website with Booking System cost to develop?"
    query_rag(text)