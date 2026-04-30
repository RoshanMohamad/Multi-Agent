# 🤖 Multi-Agent AI System

A powerful, full-stack multi-agent AI application built to solve complex tasks using collaborative LLM workflows. This system leverages **LangChain** for agent orchestration and **Ollama** for running high-performance local language models.

---

## 🏗️ Architecture Overview

The application is structured into a modern decoupled architecture:

- **Frontend**: A sleek, responsive React dashboard built with **Vite**, **TypeScript**, and **Lucide React** icons. It supports real-time SEO-optimized chat interfaces and agent switching.
- **Backend**: A high-performance **FastAPI** server that manages agent lifecycle, task execution, and persistent logging using **SQLAlchemy**.
- **Agent Layer**: Specialized agents using **LangChain** and **Ollama (Local LLMs)** like Llama 3 or Mistral.

---

## 🤖 Specialized AI Agents

### 💻 1. Software Development Team
A collaborative coding system that mimics a real engineering department:
- **Manager Agent**: Breaks down high-level feature requests into actionable technical tasks.
- **Coder Agent**: Implements logic and writes clean, modular code.
- **Reviewer Agent**: Performs rigorous code reviews and provides feedback loops for refinement.

### 🛡️ 2. Red Teaming Bot
An adversarial security system designed to battle-test AI safety:
- **Attacker Agent**: Uses creative prompt engineering to bypass safety guardrails.
- **Defender Agent**: Analyzes successful breaches and proposes security patches to harden the system.

### 📱 3. Autonomous Social Media Manager
A complete content creation and marketing pipeline:
- **Trend Monitor**: Scans for trending topics in your industry.
- **Content Creator**: Drafts engaging captions tailored for specific platforms.
- **Image Describer**: Generates high-fidelity prompts for AI image models (DALL-E, Midjourney).
- **Guardian Agent**: Ensures all content remains consistent with brand voice and values.

---

## 🚀 Key Features

- **✅ Real-time Streaming**: Watch agents "think" and collaborate in real-time via SSE streaming.
- **✅ Persistent History**: All conversations are stored in a database, allowing you to resume agent workflows across sessions.
- **✅ Local First**: Runs entirely on your hardware using Ollama—maximum privacy, zero API costs.
- **✅ Production Ready**: Includes configurations for Docker, Gunicorn, and cloud-ready environment variables.

---

## 🛠️ Setup & Installation

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Ollama** (Running locally)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
python api.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🏗️ DevOps & Deployment Infrastructure

This system is built with a production-first mindset, supporting modern DevOps practices:

### 🐳 Containerization
The app is fully containerized using **Docker** for consistent environments:
- **Backend Dockerfile**: Uses a multi-stage Python build optimized for size, running with **Gunicorn** and **Uvicorn** workers.
- **Frontend Dockerfile**: Multi-stage Node build that serves the static Vite assets via an **Nginx** reverse proxy.
- **Docker Compose**: A root-level `docker-compose.yml` orchestrates the API, frontend, and local PostgreSQL/Redis services for easy local testing.

### ⛓️ CI/CD Pipeline
Automated workflows via **GitHub Actions** (`.github/workflows/deploy.yml`):
- **Continuous Integration**: Auto-runs on push to `main`, handling dependency installation, linting, and build verification.
- **Continuous Deployment**: Prepared for automated pushes to **Amazon ECR** and triggering redeployments on **AWS App Runner** or **ECS**.

### ☁️ Infrastructure as Code (IaC)
Cloud infrastructure is managed via **Terraform** for reproducible AWS environments:
- **VPC Networking**: Custom VPC with public/private subnets and secure Routing Tables.
- **Security Groups**: Granular firewall rules restricting DB access to only the backend API.
- **Compute**: Auto-provisioned EC2 instances with `user_data` scripts to self-install Docker and Ollama.
- **Managed Database**: Amazon RDS (PostgreSQL) configuration for scalable agent memory.

---

## 🌐 How to Deploy to AWS

The Enterprise Track (Terraform + ECS)
1. Initialize Terraform in the `terraform/` directory: `terraform init`.
2. Apply the plan: `terraform apply`.
3. Use the generated `backend_public_ip` to configure your frontend environment variables.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the future of Agentic Workflows.**
