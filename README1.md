# 🚀 Medium Article Generator OS

An AI-powered multi-agent system built with **Agno AgentOS** that researches trending tech topics across multiple platforms and generates high-quality Medium-style articles.

---

## 📌 Overview

**Medium Article Generator OS** is a multi-agent research and content creation system that:

- 🔍 Conducts research from multiple sources:
  - ArXiv
  - DuckDuckGo (Web Search)
  - HackerNews
  - News Articles
  - Wikipedia
  - YouTube
- 🧠 Aggregates research using a Team Leader (Orchestrator)
- ✍️ Generates Medium-style articles
- 💾 Saves final drafts as Markdown files
- 📧 Can draft and manage emails via Gmail
- 🌐 Runs locally using AgentOS + FastAPI

---

## 🏗️ Architecture

The system uses a **Team-based multi-agent architecture**:

```
Medium Article Creation Team (Team Leader)
│
├── Archive Research Agent (Arxiv)
├── Web Search Agent (DuckDuckGo)
├── HackerNews Research Agent
├── News Article Research Agent
├── Wikipedia Research Agent
├── YouTube Research Agent
└── Gmail Agent
```

The **Team Leader**:
- Delegates research tasks
- Aggregates results
- Writes a Medium-style article
- Saves it as `.md` only after user confirmation

---

## 🖥️ Screenshots

### 🔹 AgentOS Running Locally

![AgentOS Running](./assets/agentos-running.png)

---

### 🔹 Agent Configuration Dashboard

![Agent Configuration](./assets/config-dashboard.png)

---

### 🔹 Swagger API Docs

![Swagger Docs](./assets/swagger-docs.png)

---

### 🔹 Team Visualization

![Team Graph](./assets/team-graph.png)

---

> 📁 Place your screenshots inside a folder called `assets/` in your repository and rename them accordingly:
>
> ```
> assets/
> ├── agentos-running.png
> ├── config-dashboard.png
> ├── swagger-docs.png
> └── team-graph.png
> ```

---

## 🧠 Tech Stack

- Agno Agent Framework
- AgentOS
- Mistral (mistral-large-latest)
- FastAPI
- DuckDuckGo Tools
- Arxiv Tools
- Wikipedia Tools
- Newspaper4k
- YouTube Tools
- HackerNews Tools
- Gmail Tools
- Python 3.10+

---

## 📂 Project Structure

```
medium-article-generator/
│
├── research_papers/        # Downloaded Arxiv papers
├── medium_articles/        # Generated articles (.md)
├── app.py                  # Main application file
├── .env                    # API keys
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/medium-article-generator.git
cd medium-article-generator
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

(Include any other required API keys if needed.)

---

## ▶️ Running the Application

```bash
uv run app.py
```

You will see:

```
OS running on: http://localhost:7777
```

---

### 🌐 Access Interfaces

| Interface | URL |
|-----------|------|
| AgentOS UI | https://os.agno.com/ |
| Local API | http://localhost:7777 |
| Swagger Docs | http://localhost:7777/docs |

---

## ✍️ How It Works

1. User provides a topic.
2. Team Leader delegates research tasks.
3. Research agents gather data from multiple sources.
4. Team Leader composes a Medium-style article.
5. User reviews draft.
6. On confirmation → Article saved as `.md`.

---

## 📄 Example Workflow

```
User: Write a Medium article about AI Agents in 2026.

→ Web research
→ HackerNews research
→ Wikipedia context
→ YouTube transcript summary
→ ArXiv paper search
→ Draft Medium article
→ Ask for confirmation
→ Save as markdown
```

---

## 💾 Output

Articles are saved inside:

```
/medium_articles/
```

Example:

```
medium_articles/
└── ai_agents_2026.md
```

---

## 🔐 Features

✔ Multi-agent orchestration  
✔ Research aggregation  
✔ Medium-style writing  
✔ Markdown export  
✔ Email drafting support  
✔ Agent history context  
✔ Streaming responses  
✔ Swagger API documentation  

---

## 📈 Future Improvements

- Add Reddit Research Agent
- Add Google Search Tool
- Add SEO optimization
- Add image generation support
- Deploy to cloud (Render / Railway / AWS)

---

## 👤 Author

**Debasish Pradhan**  
AI Engineer | Multi-Agent Systems Enthusiast  

---

## ⭐ Support

If you found this project helpful:

- ⭐ Star the repository
- 🍴 Fork it
- 🧠 Contribute improvements

---
