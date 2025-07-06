from fastapi import FastAPI
from backend.calendar_utils import get_free_slots, create_event
from pydantic import BaseModel
from backend.agent import run_agent

app = FastAPI()

class AgentRequest(BaseModel):
    query: str


@app.post("/agent")
def agent_endpoint(request: AgentRequest):
    try:
        reply = run_agent({
            "input": request.query,
            "chat_history": []  
        })
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}


@app.get("/slots")
def slots():
    try:
        events = get_free_slots()
        return {"events": events}
    except Exception as e:
        return {"error": str(e)}

@app.post("/book")
def book_meeting():
    try:
        start = "2025-07-07T10:00:00+05:30"
        end = "2025-07-07T10:30:00+05:30"
        link = create_event(start, end, "TailorTalk Booking")
        return {"link": link}
    except Exception as e:
        return {"error": str(e)}
