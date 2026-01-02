# 📧 AI-Powered Email Support Agent

## 📌 Project Overview

This project is an **AI-powered automated email support system** built using **FastAPI, MongoDB Atlas, and Large Language Models**.  
It automatically fetches emails, classifies them using AI, generates intelligent replies, and manages the entire processing workflow asynchronously with monitoring and admin controls.

The system is designed in a **production-ready manner**, supporting scalability, observability, authentication, and future AI training improvements.

---

## ❓ Problem Statement

Customer support teams receive a large number of repetitive emails such as billing queries, support requests, sales inquiries, and complaints.

Manual handling leads to:
- Delayed responses
- High operational cost
- Inconsistent reply quality
- No learning or improvement loop

---

## 🎯 Objectives

- Automatically fetch incoming emails
- Classify emails using AI (category, priority, summary)
- Generate contextual AI-based replies
- Store and manage all data in MongoDB Atlas
- Run email processing asynchronously
- Provide admin APIs, metrics, and training endpoints
- Enable future human-feedback-based AI improvement

---

## 🛠️ Tools & Technologies Used

### 🔧 Technology Stack

| Tool / Technology | Purpose |
|------------------|--------|
| FastAPI | Backend API framework |
| Python | Core programming language |
| MongoDB Atlas | Cloud database |
| Motor | Async MongoDB driver |
| PyMongo (SRV) | MongoDB Atlas connectivity |
| OpenAI API | Email classification & reply generation |
| LangChain | Prompt management & LLM orchestration |
| Uvicorn | ASGI server |
| JWT (OAuth2) | Authentication & authorization |
| Prometheus | Metrics & monitoring |
| Loguru | Structured logging |
| AsyncIO | Background task processing |

---

### 🧩 Usage of Each Tool in This Project

| Tool | How It Is Used in This Project |
|-----|-------------------------------|
| FastAPI | Defines REST APIs for emails, admin, workflow, and training |
| MongoDB Atlas | Stores emails, replies, workflow history, training data |
| Motor | Performs async DB operations for high performance |
| OpenAI API | Classifies emails and generates replies |
| LangChain | Manages prompts and LLM calls |
| JWT Auth | Secures admin and training endpoints |
| Prometheus | Tracks workflow duration, failures, email counts |
| Loguru | Produces structured JSON logs |
| AsyncIO | Runs background email fetch & processing loops |
| Uvicorn | Runs FastAPI server |

---

## 🔄 Flow of Working (High Level)

1. Emails are fetched and stored in MongoDB
2. Pending emails are picked by background workers
3. AI classifies each email
4. AI generates a reply
5. Reply is stored and optionally sent
6. Workflow execution history is recorded
7. Metrics are collected for monitoring

---

## ▶️ Steps to Run the Project (Local Setup)

 1️⃣ Prerequisites

- Python **3.10 or 3.11**
- MongoDB Atlas account
- OpenAI API key
- Internet connection

---

### 2️⃣ Clone the Repository

git clone <your-repo-url>
cd email_agent
3️⃣ Create Virtual Environment
python -m venv venv


Activate:

Windows : venv\Scripts\activate

Linux / Mac : source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ MongoDB Atlas Setup

Create a MongoDB Atlas Cluster

Create a database user (username + password)

Add IP access (0.0.0.0/0 for development)

Copy the connection string

Example:

MONGO_URI=mongodb+srv://email_agent:<PASSWORD>@cluster0.xxxxx.mongodb.net/email_agent?retryWrites=true&w=majority


⚠️ Important:

Replace <PASSWORD> with MongoDB database user password

Ensure database name is present (email_agent)

6️⃣ Environment Variables (.env)

Create a .env file:

OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongodb_atlas_uri
JWT_SECRET=your_secret_key
ADMIN_USERNAME=admin
ACCESS_TOKEN_EXPIRE_MINUTES=60

7️⃣ Run Database Test (Optional)
python test_db.py


Expected output:

Successfully connected to MongoDB!

8️⃣ Start the Application
uvicorn app.main:app --reload --port 8000

9️⃣ Access the APIs

API Docs:
👉 http://127.0.0.1:8000/docs

Health Check:
👉 http://127.0.0.1:8000/health

Metrics:
👉 http://127.0.0.1:8000/metrics




## *🔐 Authentication*

Admin APIs are protected using JWT

Login endpoint provides access token

Token must be passed as Authorization: Bearer <token>

# **📊 Monitoring & Metrics**

The system exposes Prometheus metrics:

Emails processed

Emails sent / failed

Workflow failures

Workflow execution duration

Concurrent workflow count

# **🧪 Training & Feedback (RLHF)**

The project includes scaffolding for:

Auto-labeling emails

Human review of AI outputs

Reward-based feedback

Fine-tuning dataset generation

# **✅ Final Outcome**

Fully working AI-powered email automation backend

Cloud database integration

Async workflow execution

Secure admin access

Metrics and observability

Scalable and extensible design

🚀 Future Enhancements

UI Dashboard

WhatsApp / Slack notifications

Advanced RAG with vector DB

AI fine-tuning

SLA-based escalation

# **🏁 Conclusion**

This project demonstrates a real-world AI backend system using modern tools and best practices.
It is suitable for academic projects, portfolios, and real production use cases.

