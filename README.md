# SHL Assessment Recommendation System

An enterprise-grade Generative AI–powered web application that converts natural-language queries or job descriptions into a ranked list (up to 10) of tailored SHL assessment solutions. By leveraging large language models, vector embeddings, and a high-performance retrieval layer, this system delivers actionable metadata to streamline and automate your talent-screening workflow.

---

## 🚀 Live Demo & Documentation

- **Live Demo:** https://demo.yourdomain.com  
- **API Documentation (Swagger UI):** https://api.yourdomain.com/docs  

---

## 🔑 Key Features

- **Natural-Language Interface**  
  Accepts free-text queries or job description URLs and interprets hiring requirements with semantic precision.
- **Top-K Recommendations**  
  Returns up to 10 highly relevant SHL assessments ranked by contextual relevance and business constraints.
- **Comprehensive Metadata**  
  For each recommendation, exposes:
  - **Assessment Name & Catalog URL**  
  - **Remote Testing Support** (Yes / No)  
  - **Adaptive/IRT Support** (Yes / No)  
  - **Duration** & **Test Type**
- **RESTful API**  
  - `GET /health` — Service health check  
  - `POST /recommend` — JSON-based recommendation endpoint  
- **Scalable Embedding Store**  
  Integrates with FAISS or Pinecone for sub-second vector retrieval at scale.
- **Modular Architecture**  
  Backend (FastAPI) + Frontend (Streamlit) + Embedding Layer + LLM Inference.

---

## 🛠️ Tech Stack

| Layer                | Technology                   |
|----------------------|------------------------------|
| **Backend API**      | Python 3.10, FastAPI         |
| **LLM Provider**     | OpenAI GPT-4 / Google Gemini |
| **Vector Store**     | FAISS / Pinecone             |
| **Frontend UI**      | Streamlit                    |
| **Testing**          | pytest                       |
| **CI/CD**            | GitHub Actions               |

---

## 📦 Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/<your-username>/shl-assessment-recommender.git
   cd shl-assessment-recommender
