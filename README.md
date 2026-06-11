
# S사 AI Agent Project - Test Operation Efficiency

Sample FastAPI + LangGraph Agent for AI-driven test operation innovation.
This project combines FastAPI, LangGraph, PostgreSQL, and a lightweight developer workflow for test operation tooling.

## What This Project Is

- FastAPI backend with an `/agent/query` endpoint
- LangGraph-based agent flow with PostgreSQL chat history
- Dockerized PostgreSQL and pgAdmin for local development
- `uv`-based Python environment management
- Local fallback mode when `OPENAI_API_KEY` is not set

## Project Layout

- `app/main.py`: FastAPI entrypoint and API routes
- `agents/test_agent.py`: agent graph, model selection, persistence flow
- `db/database.py`: SQLAlchemy engine, session, and `ChatHistory`
- `tools/test_tools.py`: reusable tool examples
- `test_db.py`: database smoke test
- `test_agent_api.py`: direct `/agent/query` client script
- `docker-compose.yml`: PostgreSQL and pgAdmin stack

## Prerequisites

- Python 3.10+
- Docker Desktop running
- PowerShell 7+ on Windows recommended
- `uv` installed

## Setup

### Windows

```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv venv .venv
.venv\Scripts\Activate.ps1
uv sync --dev
```

### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
source .venv/bin/activate
uv sync --dev
```

### Optional pip Flow

```bash
pip install -r requirements.txt
```

## Environment Variables

Use `.env` locally. Do not commit it.

- `OPENAI_API_KEY`: required for OpenAI-backed responses
- `DATABASE_URL`: default is `postgresql://user:password@localhost:5432/hynix_test_db`

If `OPENAI_API_KEY` is missing, the agent returns a local fallback response so developers can still test the full request flow.

## Start Local Services

```bash
docker-compose up -d
```

This starts:

- PostgreSQL on port `5432`
- pgAdmin on port `8080`

## Verify the Database

```bash
uv run python test_db.py
```

Expected result:

- PostgreSQL connection succeeds
- `chat_history` table is created
- basic row-count query succeeds

## Run the API

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
http://localhost:8000/health
```

## Agent Testing

### Direct Endpoint Test

```bash
uv run python test_agent_api.py "현재 테스트 상태를 요약해줘" --session-id test-001
```

### PowerShell One-liner

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8000/agent/query" `
  -ContentType "application/json" `
  -Body '{"query":"현재 테스트 상태를 요약해줘","session_id":"test-001"}'
```

## pgAdmin Settings

Open `http://localhost:8080` and log in with:

- Email: `admin@skhynix.com`
- Password: `admin`

Register the PostgreSQL server with:

- Host: `db`
- Port: `5432`
- Username: `user`
- Password: `password`
- Database: `hynix_test_db`

Use `localhost` only when a tool is running directly on the host machine, not from inside pgAdmin.

## Daily Developer Workflow

1. Pull or sync the latest branch.
2. Activate the virtual environment.
3. Start Docker services.
4. Run `test_db.py` and confirm PostgreSQL is healthy.
5. Start the API server.
6. Use `test_agent_api.py` or `/agent/query` to verify behavior.
7. Make code changes in small increments.
8. Re-run the smoke tests before pushing.

## Development Guidelines

- Keep `.env` and `.venv` out of Git.
- Update `README.md` when the startup flow or required env vars change.
- Prefer `uv run ...` for reproducible command execution.
- Use the fallback mode for local validation when OpenAI credentials are unavailable.
- Keep database schema changes intentional and test them with `test_db.py`.

## GitHub Workflow

Create the GitHub repository first, then connect and push from the local repo.

```powershell
cd c:\skh_ai_agent
git status
git add .
git commit -m "Initial project setup"
git branch -M main
git remote add origin https://github.com/koco-ai/skh_ai_agent.git
git push -u origin main
```

If the remote already exists:

```powershell
git remote set-url origin https://github.com/koco-ai/skh_ai_agent.git
git push -u origin main
```

## License and README Policy

- Do not create a second README on GitHub if this local README already exists.
- For internal use, choose no license.
- For public use, MIT is the simplest default.
- Never commit `.env` or any secret values.

## Troubleshooting

- If `git status` says the repo is not initialized, run `git init` in `c:\skh_ai_agent`.
- If pgAdmin cannot connect, make sure the server host is `db`, not `localhost`.
- If `/agent/query` returns a 500 error, check `OPENAI_API_KEY` and confirm Docker/PostgreSQL are running.
- If PowerShell output looks garbled, use `test_agent_api.py` to print JSON cleanly.