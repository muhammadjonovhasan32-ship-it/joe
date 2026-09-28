import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Joe AI", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    reply: str


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY muhit o'zgaruvchisi o'rnatilmagan.",
        )
    return OpenAI(api_key=api_key)


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = get_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Siz foydali, halol va qisqa javob beradigan AI yordamchisiz.",
                },
                {"role": "user", "content": request.message},
            ],
        )
        reply = response.choices[0].message.content or "Javob olinmadi."
        return ChatResponse(reply=reply)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"OpenAI xatosi: {error}") from error
