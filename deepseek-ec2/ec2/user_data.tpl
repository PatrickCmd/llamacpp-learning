#!/usr/bin/env bash
set -e

apt-get update
apt install -y git
apt install python3-pip -y
apt install python3.12-venv -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
nohup ollama serve > /home/ubuntu/ollama.log 2>&1 &

# Wait for ollama to be ready
sleep 10

# Pull models as the ollama user
ollama pull deepseek-r1:8b
ollama pull gemma3
ollama pull qwen3:8b
ollama pull mxbai-embed-large
ollama pull nomic-embed-text

# Clone repository
cd /home/ubuntu
sudo -u
git clone https://github.com/PatrickCmd/llamacpp-learning.git
cd llamacpp-learning/deepseek-ec2

# Install dependencies
python3 -m venv env
bash -c "source env/bin/activate && pip install --upgrade pip"
bash -c "source env/bin/activate && pip install -r requirements.txt"

# Start streamlit (run in background)
bash -c "cd /home/ubuntu/llamacpp-learning/deepseek-ec2 && source env/bin/activate && nohup streamlit run app.py --server.address 0.0.0.0 --server.port 8501 > /var/log/streamlit.log 2>&1 &"

# Log completion
echo "Setup completed successfully at $(date)" >> /var/log/user-data.log