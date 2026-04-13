# 🧠 Agentic AI Research & Analysis Assistant
### *Bridging Statistical Rigor and Autonomous Reasoning*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/ORCHESTRATION-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/Inference-Groq-green.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Project Overview
The **Agentic AI Research Assistant** is a next-generation research platform designed to automate the lifecycle of academic and web-based research. By combining traditional **Statistical NLP** founded in Milestone 1 with a cutting-edge **Autonomous Agentic Flow** in Milestone 2, the system provides both explainable insights and deep-reasoning capabilities.

The assistant doesn't just search the web; it **thinks**. It evaluates its own research, identifies information gaps, and autonomously decides whether to loop back for more data or synthesize its findings into a professional, research-grade report.

---

## 🏗️ Technical Architecture (Milestone 2)

The core engine is built on a **Node-Based State Machine** orchestrated by **LangGraph**. This mimics the human research process of iteration and refinement.

```mermaid
graph TD
    Start([User Query]) --> Search[Search Node]
    Search --> Fetch[Fetch Node]
    Fetch --> Summarize[Summarize Node]
    Summarize --> Analyze[Analyze Node]
    Analyze --> Decision{Enough Info?}
    Decision -- NO --> Search
    Decision -- YES --> Extract[Fact Extraction Node]
    Extract --> Report[Report Node]
    Report --> End([Final Markdown Report])
```

---

## ✨ Features (Member-Specific Work)

### 📡 Data & Discovery (Member 1 - Akhilesh)
*   **Hybrid Search Engine**: Integrates **Tavily AI** (Premium), **DuckDuckGo**, and **ArXiv** for a "Best of Both Worlds" search strategy.
*   **Smart Fetching**: Clean content extraction from complex websites using BeautifulSoup with noise-reduction logic.

### 🧠 Agent Logic & Orchestration (Member 2 - Lakshya)
*   **Autonomous Decision Loop**: The agent evaluates its own findings. If the topic is too complex, it automatically iterates to find more data.
*   **Hard-Fact Extraction**: Isolates critical technical data (numbers, dates, percentages) into a professional **Research at a Glance** table.
*   **Token-Preserving State**: Centralized state management that intelligently hands off data between nodes.

### ✍️ Intelligent Synthesis (Member 3 - Dhruv)
*   **Tiered LLM Architecture**: 
    *   **Llama-3.1-8B**: Lightning-fast, cost-effective extraction for summaries.
    *   **Llama-3.3-70B**: High-reasoning synthesis for the final final report.
*   **Local NLP Pre-Filtering**: Uses local TextRank/Keyword ranking to reduce webpage "junk" before sending it to the API, saving up to 80% on token costs.

---

## 🛠️ Getting Started

### 1. Environment Setup
Create a `.env` file in the root directory:
```bash
# --- LLM Architecture ---
GROQ_API_KEY=your_groq_key
MODEL_NAME=llama-3.3-70b-versatile

# --- Search Intelligence ---
TAVILY_API_KEY=your_tavily_key  # Optional: For Best-of-Best results

# --- App Config ---
HF_TOKEN=your_huggingface_token
```

### 2. Installation
```bash
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
```

### 3. Usage
**Full Agentic Flow (Current):**
```bash
python3 milestone_2/test_full_flow.py "Latest breakthroughs in Carbon Capture 2024"
```

---

## 👥 Meet the Team

| Team Member | Role | Contribution |
| :--- | :--- | :--- |
| **Akhilesh Kumar** | **Data Architect** | Real-time Search Integration & Web Scraping |
| **Lakshya Agarwal** | **Workflow Strategist** | LangGraph Orchestration & Decision Logic |
| **Dhruv Ramani** | **Intelligence Engineer** | LLM Optimization & Research Synthesis |

---

## 🔭 Future Roadmap (Milestone 3)
*   **Interactive Dashboard**: A state-of-the-art Streamlit UI for real-time research visualization.
*   **Chat Memory**: Interactive follow-up questions about the research report.
*   **Multi-Format Export**: One-click download of reports as PDF or LaTeX.

---

> [!NOTE]
> This project was developed as part of a high-performance Agentic AI training curriculum. For support or contributions, please contact the development team.
