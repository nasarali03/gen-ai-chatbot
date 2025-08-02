from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from gemini import MentalHealthAssistant
import uvicorn

app = FastAPI()

# Initialize the mental health assistant
mental_health_assistant = MentalHealthAssistant()

# Pydantic models for request and response
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="User's mental health message")
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty or only whitespace')
        return v.strip()

class ChatResponse(BaseModel):
    message: str = Field(..., description="AI response message")

@app.get("/")
def read_root():
    return {"message": "Hi this is mental health supprt chatbot powered by Gemini"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        user_input = request.message
        response_text = mental_health_assistant.get_mental_health_response(user_input)
        return ChatResponse(message=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)