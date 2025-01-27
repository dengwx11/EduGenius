from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from agents.agent_manager import AgentManager

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent manager
agent_manager = AgentManager()

class OutlineRequest(BaseModel):
    outline: str

@app.post("/api/generate")
async def generate_content(request: OutlineRequest) -> Dict[str, Any]:
    """Generate PPT and lesson plan content from an outline"""
    try:
        content = agent_manager.generate_content(request.outline)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
