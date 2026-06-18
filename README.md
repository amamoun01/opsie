# Opsie: Cloud-Native ChatOps Automation Engine

<!-- markdownlint-disable MD033 -->
<p align="center">
  <img src="https://github.com/amamoun01/opsie/blob/main/assets/opsie-avatar.png" width="200" alt="Opsie Logo">
</p>
<!-- markdownlint-enable MD033 -->

A lightweight asynchronous [ChatOps](https://www.geeksforgeeks.org/devops/chatops/) microservice architecture designed to route, evaluate, and fulfill operational infrastructure commands directly from Discord utilizing dynamic multi-model LLM orchestration ([OpenAI](https://developers.openai.com/api/docs) and [Gemini](https://ai.google.dev/gemini-api/docs)).

<!-- ## 🎥 Quick Demo

![Opsie ChatOps Demo](assets/demo.gif)

--- -->

## 🏗️ System Architecture

* **Orchestration Mesh:** Built on a completely decoupled microservice architecture consisting of an asynchronous `discord.py` bot client layer and a high-performance **FastAPI** backend API.

* **Dynamic Model Routing:** Features an adaptive inference broker utilizing **LiteLLM** to seamlessly hot-swap and route incoming requests between multiple upstream providers (**OpenAI gpt-4o-mini**, **Google Gemini 2.5 Flash**) based on runtime channel overrides.

* **Production Observability:** Implements custom operational telemetry middleware that intercepts raw application traffic and structures logging payloads into flat JSON schemas outputted directly to `stdout` for modern log-aggregators.

![Architecture Diagram](https://github.com/amamoun01/opsie/blob/main/assets/opsie_architecture.png)

## 🚀 Quick Start

### 1. Configure the environment

Clone the repository and instantiate your environment variables from the configuration profile template:

```bash
cp .env.example .env
```

Open `.env` and populate your secure infrastructure tokens:

```text
OPENAI_API_KEY=sk-proj-...
GEMINI_API_KEY=AIzaSy...
DISCORD_BOT_TOKEN=MTIy...
```

> Ensure you navigate to the Discord Developer Portal under your application's "Bot" tab and toggle the Message Content Intent security switch to `ON`.

### 2. Initialize the Local Workspace

The repository provides a centralized automation task runner interface via [GNU Make](https://make.mad-scientist.net/) to abstract and standardize developer setup workflows:

```bash
# Init virtual environments, pull configurations, and install pre-commit hooks
make init
```

### 3. Spin Up the Containerized Topologies

Compile and launch your decoupled application containers simultaneously in detached mode leveraging localized BuildKit caching layers:

```bash
# Build and run the service architecture mesh
make up

# Stream unified stdout application logs from all running services
make logs
```

## 🛠️ Management & Automation

| Command | Action |
| :--- | :--- |
| `make init` | Provisions local python virtual environments and registers local pre-commit tracking hooks. |
| `make up` | Compiles application container layers and launches the service overlay network. |
| `make down` | Demolishes container topologies, prunes virtual interfaces, and removes orphan layers. |
| `make restart` | Executes a clean sequence tear down followed by an immediate structural rebuild. |
| `make logs` | Attaching to unified standard output log streams. |

---

## 🛡️ CI/CD Quality Gates & DevSecOps

The repository implements a comprehensive, multi-track GitHub Actions continuous integration workflow to guarantee software supply chain integrity before merging code:

* **Static Analysis**: Uses [`Ruff`](https://docs.astral.sh/ruff/) to validate Python linting, code quality, style uniformity, and syntax formatting rules.

* **Security & Vulnerability Scanning**: Integrates [`Trivy`](https://trivy.dev/docs/latest/guide/) to scan filesystem dependencies for high/critical CVE risks and accidental credential exposures.

* **Compilation Integrity**: Executes a structural dry-run build of the Docker configurations to ensure the infrastructure layout compiles safely before deployment.

## 🔮 Next Steps & Scaling Roadmap

To transition **`Opsie`** from an interactive chatbot into a hardened infrastructure controller, the following milestones are actively being engineered:

* **Secure Tool Execution (Function Calling)**: Extend the FastAPI backend to support JSON tool definitions. This allows the bot-driven AI to safely run read-only terminal commands (e.g., `kubectl get pods`) directly from chat.

* **Stateful Session Layer ([Redis](https://redis.io/docs/latest/))**: Move chat history out of volatile application memory and into a local Redis service. This lets you horizontally scale your backend API nodes without losing conversational context.

* **Secret Configuration Management**: Migrate sensitive credentials out of plain `.env` files and integrate a secure injection pattern using tools like [HashiCorp Vault](https://developer.hashicorp.com/vault) or [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).

* **Kubernetes Orchestration & Deployment**: Migrate the containerized services from Docker Compose into a managed Kubernetes cluster, creating declarative manifest layouts (*Deployments*, *Services*, and *ConfigMaps*) for automated, scalable hosting.
