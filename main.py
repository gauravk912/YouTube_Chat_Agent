from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import ask_video_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open for dev
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    video_id: str
    query: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    try:
        print(f"📺 Received: video_id={req.video_id} | query='{req.query}'")
        answer = ask_video_question(req.video_id, req.query)
        return {"answer": answer}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
