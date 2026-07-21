# 🤖 Roshab AI — Universal Agentic AI Operating System

Roshab AI is a production-grade, enterprise-ready Universal Agentic AI Operating System. Designed with clean architecture, high scalability, and strict security controls, Roshab AI coordinates specialized agents, executes complex multi-step plans, interfaces with tools and Model Context Protocol (MCP) servers, and manages short/long-term memory dynamically.

---

## 🌟 Key Features

* **🧠 Multi-Agent Orchestration:** Powered by state-graph workflows (LangGraph) with delegated task handling via Manager, Coding, Research, and Security agents.
* **🔒 Enterprise Security & RBAC:** Role-Based Access Control (Admin, Operator, Developer, Viewer) with built-in Human-in-the-Loop (HITL) approval layers for high-risk execution tasks.
* **⚡ Modern Async Stack:** High-performance REST & WebSocket APIs powered by FastAPI, SQLAlchemy (Async), and Redis.
* **🌐 Web Automation & Tools:** Native Playwright support for headless browser navigation, form fills, data scraping, and isolated code execution.
* **🧠 Multi-Tiered Memory:** Vector search memory powered by Qdrant combined with short-term contextual history.
* **🔌 MCP & Plugin Infrastructure:** Native Model Context Protocol (MCP) support for external integrations (GitHub, Slack, Databases, Local System).

---

## 📁 Repository Structure

```text
roshab-ai/
├── agents/                  # Specialized autonomous agents (Manager, Coding, etc.)
├── backend/
│   ├── api/                 # REST endpoints, WebSocket hubs, & RBAC auth
│   ├── config/              # App settings, logging, & security configs
│   ├── core/                # Brain, Planner, Intent Routers & Security Engine
│   ├── database/            # Async Postgres, Redis, Vector DB, & User Models
│   └── main.py              # Application entry point
├── docker/                  # Container deployment files
├── memory/                  # Semantic search & memory compression logic
├── plugins/                 # Extensible tool plugins
├── tests/                   # Unit & integration test suite
├── .env.example             # Environment template
├── pyproject.toml           # Poetry dependencies configuration
└── requirements.txt         # Standard pip requirements