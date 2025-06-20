import os

from langchain_aws import BedrockEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

IS_USING_IMAGE_RUNTIME = bool(os.environ.get("IS_USING_IMAGE_RUNTIME", False))

if IS_USING_IMAGE_RUNTIME:
    os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"
    os.environ["HF_HOME"] = "/tmp/huggingface"

HF_EMBED_MODEL_ID = "BAAI/bge-small-en-v1.5"


# Wrapper that tries Bedrock embeddings first, falls back to HuggingFace on errors
class FallbackEmbeddings:
    def __init__(self, bedrock_model_id: str, hf_model_id: str):
        self.bedrock = BedrockEmbeddings(model_id=bedrock_model_id)

        if IS_USING_IMAGE_RUNTIME:
            # Ensure HuggingFace cache is set to a writable location in Lambda
            self.hf = HuggingFaceEmbeddings(model_name=hf_model_id, cache_folder="/tmp/huggingface")
        else:
            # Use default cache location for local or non-Lambda environments   
            self.hf = HuggingFaceEmbeddings(model_name=hf_model_id)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        try:
            return self.bedrock.embed_documents(documents)
        except Exception as e:
            print(f"Bedrock embedding failed: {e}. Falling back to HuggingFace.")
            return self.hf.embed_documents(documents)

    def embed_query(self, query: str) -> list[float]:
        try:
            return self.bedrock.embed_query(query)
        except Exception as e:
            print(f"Bedrock query embedding failed: {e}. Falling back to HuggingFace.")
            return self.hf.embed_query(query)


def get_embedding_function():
    # Return a fallback embedding instance that handles runtime failures
    return FallbackEmbeddings(
        bedrock_model_id="amazon.titan-embed-text-v2:0",
        hf_model_id=HF_EMBED_MODEL_ID,
    )