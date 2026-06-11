import operator
import os
from contextlib import contextmanager
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from db.database import ChatHistory, get_db_session

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    session_id: str

class TestAgent:
    def __init__(self):
        self.use_openai = bool(os.getenv("OPENAI_API_KEY")) and ChatOpenAI is not None
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) if self.use_openai else None
        self.graph = self.build_graph()

    def build_graph(self):
        workflow = StateGraph(AgentState)
        
        def agent_node(state: AgentState):
            messages = state["messages"]
            if self.use_openai:
                response = self.llm.invoke(messages)
                return {"messages": [response]}

            query = messages[-1].content
            response_text = (
                "로컬 모드 응답입니다. "
                f"질문 '{query}' 를 받았습니다. "
                "OPENAI_API_KEY가 설정되면 실제 LLM 응답으로 전환됩니다."
            )
            return {"messages": [HumanMessage(content=response_text)]}
        
        workflow.add_node("agent", agent_node)
        workflow.set_entry_point("agent")
        workflow.add_edge("agent", END)
        
        return workflow.compile()
    
    @contextmanager
    def get_db(self):
        db = next(get_db_session())
        try:
            yield db
        finally:
            db.close()
    
    def invoke(self, query: str, session_id: str = "default"):
        with self.get_db() as db:
            # Save query
            history = ChatHistory(session_id=session_id, query=query)
            db.add(history)
            db.commit()
        
        state = {"messages": [HumanMessage(content=query)], "session_id": session_id}
        result = self.graph.invoke(state)
        
        response_text = result["messages"][-1].content
        
        with self.get_db() as db:
            # Update with response
            history = ChatHistory(session_id=session_id, query=query, response=response_text)
            db.add(history)  # Simplified, better to update
            db.commit()
        
        return response_text
