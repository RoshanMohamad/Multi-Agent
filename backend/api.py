import asyncio
import json
import os
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db, ChatLog

# Import agents
from red_teaming_bot import RedTeamingSystem
from social_media_manager import SocialMediaManager
from software_dev_team import SoftwareDevTeam

app = FastAPI()

# Enable CORS for the React frontend
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = [frontend_url] if frontend_url != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    username: str = "anonymous"
    agent: str
    message: str

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

async def mock_streaming_response(text: str) -> AsyncGenerator[str, None]:
    """Simulates streaming response based on the agent's full output."""
    # Split text into chunks to simulate streaming
    # In a real app, this would come from the LLM's stream method
    words = text.split(' ')
    for i in range(len(words)):
        chunk = words[i] + (' ' if i < len(words) - 1 else '')
        yield f"data: {json.dumps({'text': chunk})}\n\n"
        await asyncio.sleep(0.05)

@app.get("/api/chat/history")
async def get_chat_history(agent_id: str, username: str, db: Session = Depends(get_db)):
    logs = db.query(ChatLog).filter(
        ChatLog.agent_id == agent_id,
        ChatLog.username == username
    ).order_by(ChatLog.created_at.asc()).all()
    
    history = []
    for log in logs:
        history.append({"role": "user", "content": log.user_message})
        history.append({"role": "bot", "content": log.bot_response})
        
    return {"history": history}

@app.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    username = request.username
    agent_id = request.agent
    message = request.message
    
    # Simple logic to route to the correct agent
    # Since existing agents work synchronously, we'll wrap their calls
    # and stream the result back
    
    try:
        if agent_id == "general":
            # For general, just return a simple acknowledgment or implement a simple LLM call
            from langchain_ollama import OllamaLLM
            import config
            llm = OllamaLLM(base_url=config.OLLAMA_BASE_URL, model=config.OLLAMA_MODEL)
            # Full response for simplicity, then chunk it
            # In production, use llm.stream()
            response = await asyncio.to_thread(llm.invoke, message)
            
        elif agent_id == "coder":
            team = SoftwareDevTeam()
            response = await asyncio.to_thread(team.develop_feature, message, max_iterations=1)
            
        elif agent_id == "red_team":
            system = RedTeamingSystem()
            # Redirect stdout to capture agent conversation? 
            # Or just return the final patches. 
            # Existing system prints a lot to console.
            # We'll just run it and return the objective result for now.
            response = await asyncio.to_thread(system.run_red_team_exercise, message, max_rounds=1)
            # Hack: return the patches as response
            response = f"Exercise complete for: {message}\n\nApplied Patches:\n{system.patches or 'None'}"
            
        elif agent_id == "social":
            brand_guidelines = {
                "Voice": "Professional yet friendly",
                "Tone": "Innovative",
                "Values": "Innovation, trust"
            }
            manager = SocialMediaManager(brand_guidelines)
            result = await asyncio.to_thread(manager.create_post, industry="Gen AI", brand_voice="Pro", platform="Twitter", target_audience="Techies", max_iterations=1)
            if result:
                response = f"Post Ready!\n\nCaption: {result['caption']}\n\nImage Prompt: {result['image_prompt']}"
            else:
                response = "Could not generate approved content."
        else:
            response = "Unknown agent selected."
            
        # Log conversation to Database (Ready for RDS)
        try:
            log_entry = ChatLog(
                username=username,
                agent_id=agent_id,
                user_message=message,
                bot_response=response
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_err:
            print(f"Error logging to DB: {db_err}")
            
        return StreamingResponse(mock_streaming_response(response), media_type="text/event-stream")
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        async def error_stream():
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # Note: In production, it is recommended to run via a proper process manager like gunicorn:
    # gunicorn -k uvicorn.workers.UvicornWorker api:app -w 4 -b 0.0.0.0:8000
    uvicorn.run(app, host=host, port=port)
