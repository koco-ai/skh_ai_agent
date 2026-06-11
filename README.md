# SK Hynix AI Agent Project - Test Operation Efficiency
- DB test script + pgAdmin viewer
- Extensible tools for TEST operation efficiency (SK Hynix)


## Overview
Sample FastAPI + LangGraph Agent for AI-driven test operation innovation.
Demonstrates Langchain/LangGraph, FastAPI, PostgreSQL integration.

## Setup (uv 추천 - 빠르고 현대적인 방식)

**Windows 사용자 주의사항**:
- Docker Desktop을 설치하고 실행 중이어야 합니다.
- PowerShell을 **관리자 권한**으로 실행하는 것을 추천합니다.
- Windows Terminal + PowerShell 7+ 권장.

### uv 사용 방법 (권장)

#### Windows 사용자 (PowerShell 추천)
```powershell
# 1. uv 설치 (PowerShell에서 실행)
irm https://astral.sh/uv/install.ps1 | iex

# 2. 프로젝트 디렉토리로 이동 후 가상환경 생성
uv venv .venv

# 3. 가상환경 활성화
.venv\Scripts\Activate.ps1

# 4. 의존성 설치
uv sync --dev
```

#### Linux / macOS
```bash
# 1. uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 가상환경 생성 및 활성화
uv venv .venv
source .venv/bin/activate

# 3. 의존성 설치
uv sync --dev
```

### 기존 pip 방식
```bash
pip install -r requirements.txt
```

2. `.env.example`을 `.env`로 복사하고 키 입력 (OPENAI_API_KEY, DATABASE_URL)

3. Docker 서비스 시작 (PostgreSQL + pgAdmin):
   ```bash
   docker-compose up -d
   ```

4. DB 연결 테스트:
   ```bash
   uv run python test_db.py     # 또는 python test_db.py (활성화된 venv)
   ```

  

5. FastAPI 실행:
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```

## DB Viewer (pgAdmin)
- Access: http://localhost:8080
- Email: admin@skhynix.com
- Password: admin
- Add Server: Host=`db`, Port=5432, Username=`user`, Password=`password`
- Use `localhost` only when connecting from a tool running on the host machine, not from pgAdmin inside Docker
- Database: `hynix_test_db`

## Endpoints
- POST /agent/query : Query the AI Agent
- GET /health

## Features
- LangGraph Agent with state management & PostgreSQL chat history
- FastAPI Backend with middleware-ready structure브라우저에서 확인합니다.

## 브라우저에서 확인
http://localhost:8000/health
pgAdmin에서 hynix_test_db가 보이는지 확인
/agent/query가 있으면 실제 쿼리도 한 번 보내서 응답을 봅니다.


 `/agent/query` 직접 호출 테스트:
   ```bash
   uv run python test_agent_api.py "현재 테스트 상태를 요약해줘"
   ```





## git 관련
.env는 GitHub에 올리지 않습니다.
.env.example만 올리고
실제 .env는 로컬에만 둡니다
지금 보이는 OPENAI_API_KEY가 실제 키라면 GitHub 올리기 전에 교체하는 게 안전합니다

## GitHub 올리는 과정
koco-ai 조직 아래 저장소로 올리는 기준입니다.

1. Git 상태를 확인합니다.

git status

실패시 먼저 저장소 루트에서 한 번 초기화
cd c:\skh_ai_agent
git init
git status

2. .gitignore에 .env, .venv, pycache 같은 민감 파일이 들어가 있는지 확인합니다.


그다음부터는 항상 같은 폴더에서 git status, git add, git commit을 하시면 됩니다. 이미 GitHub 저장소에 올릴 계획이면 git init 후에 git remote add origin ...을 붙이면 됩니다.