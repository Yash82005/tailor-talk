from langchain_groq import ChatGroq 
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from backend.calendar_utils import get_free_slots, create_event
from datetime import datetime, timedelta
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama3-8b-8192",
)

def get_slots_text(_):  
    events = get_free_slots()
    if not events:
        return "You're completely free! No events found."
    return "\n".join([e['start']['dateTime'] for e in events])


def book_dummy_event(_):
    start = "2025-07-07T16:00:00+05:30"
    end = "2025-07-07T16:30:00+05:30"
    link = create_event(start, end, "LangChain Meeting")
    return f"Meeting booked! Join link: {link}"

tools = [
    Tool(
        name="GetCalendarSlots",
        func=get_slots_text,
        description="Use this to see available calendar slots."
    ),
    Tool(
        name="BookMeeting",
        func=book_dummy_event,
        description="Use this to book a meeting at a default time."
    )
]

agent = initialize_agent(
    tools, llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)

def run_agent(input_dict):
    return agent.run(input_dict)
