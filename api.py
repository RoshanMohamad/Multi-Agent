import asyncio
import json
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import agents
from red_teaming_bot import RedTeamingSystem
from social_media_manager import SocialMediaManager
from software_dev_team import SoftwareDevTeam

app = FastAPI()

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
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

@app.post("/api/chat")
async def chat(request: ChatRequest):
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
            
        return StreamingResponse(mock_streaming_response(response), media_type="text/event-stream")
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        async def error_stream():
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
