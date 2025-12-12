# AI Infrastructure Chatbot 🧠☁️

An **LLM-powered assistant** that converts natural language into **production-ready Terraform code** for AWS—and safely simulates `terraform plan`.

> ✨ _"Create a VPC with 2 public subnets in us-east-1"_ → Valid Terraform + Execution Plan

## 🔧 Tech Stack
- **LLM**: Google Gemini 2.0 Flash (via LangChain)
- **Cloud**: AWS (Terraform provider)
- **Safety**: Isolated temp dir, 30s timeout, **no auto-apply**
- **Environment**: GitHub Codespaces (fully reproducible)

## ▶️ How to Run
```bash
# 1. Setup
cp .env.example .env  # add your GOOGLE_API_KEY
pip install -r requirements.txt

# 2. Run
python src/main.py

# 3. Run in web UI
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload