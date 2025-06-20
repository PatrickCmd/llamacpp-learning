FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Required to make SQLlite3 work for Chroma.
RUN pip install pysqlite3-binary

# Install the specified packages
RUN pip install -r requirements.txt --upgrade

# Download and cache model
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Set HuggingFace cache to a writable location
ENV TRANSFORMERS_CACHE=/tmp/huggingface
ENV HF_HOME=/tmp/huggingface

# For local testing.
EXPOSE 8000

# Set IS_USING_IMAGE_RUNTIME Environment Variable
ENV IS_USING_IMAGE_RUNTIME=True

# Copy all files in ./src
COPY src/* ${LAMBDA_TASK_ROOT}
COPY src/rag_app ${LAMBDA_TASK_ROOT}/rag_app
COPY src/data/chroma ${LAMBDA_TASK_ROOT}/data/chroma
