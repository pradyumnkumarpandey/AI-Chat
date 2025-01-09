from fastapi import FastAPI, WebSocket
from google_gemini import get_gemini_reponse
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import os
app = FastAPI()

templates = Jinja2Templates(directory="templates")

templates = Jinja2Templates(directory=os.path.abspath(os.path.dirname(__file__)))

@app.get("/", response_class=HTMLResponse)
async def render_html(request: Request):
    return templates.TemplateResponse("design.html", {"request": request})


@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            ai_reponse = get_gemini_reponse(data)
            await websocket.send_text(f"AI:  {ai_reponse}")
    except Exception as e:
        print(e)
        print("Client disconnected.")
