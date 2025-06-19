# Deploy DeepSeek on EC2
[Youtube](https://www.youtube.com/watch?v=_jXeIxVUVnw)

- Ubuntu 24.04 lts
- g4dn.xlarge
- 2 volumes (165 each) gp3
- Security Group Rules
    SSH Anywhere
    HTTP/S AnyWhere
    Custom TCP (11434 and 8501) Anywhere

```ssh
ssh -i "../exp-net-fundamentals-2025-Q2/projects/key-pairs/nwtbootcampkey-pem.pem" ubuntu@ec2-34-204-183-145.compute-1.amazonaws.com
```

### Update Instance and Install Required Packages

```sh
mkdir deepseek-app && cd deepseek-app
sudo su
apt-get update
apt install python3-pip -y
apt install python3.12-venv -y

### Install ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull deepseek-r1:8b
ollama pull gemma3
ollama pull qwen3:8b

### Install Dependencies
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### List models

```sh
ollama list
```

#### Send request


```sh
# List models
curl http://localhost:11434/api/tags | python3 -m json.tool
curl http://34.204.183.145:11434/api/tags | python3 -m json.tool
```


```sh
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "What is an LLM?"}],
  "stream": false
}' | python3 -m json.tool
```

```sh
curl http://34.204.183.145:11434/api/chat -d '{
  "model": "qwen3:8b",
  "messages": [{"role": "user", "content": "What is an LLM?"}],
  "stream": false
}' | python3 -m json.tool
```