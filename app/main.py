from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agents.test_agent import TestAgent
from db.database import get_db_session, init_db

load_dotenv()

app = FastAPI(title="SK Hynix AI Agent for Test Operation Efficiency")

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

class Response(BaseModel):
    response: str
    session_id: str

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/agent/query", response_model=Response)
async def query_agent(request: QueryRequest):
    try:
        agent = TestAgent()
        result = agent.invoke(request.query, request.session_id)
        return Response(response=result, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
