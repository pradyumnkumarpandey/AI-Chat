from fastapi import FastAPI, WebSocket
from google_gemini import get_gemini_reponse
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import os
from fastapi.middleware.cors import CORSMiddleware
import logging
logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
templates = Jinja2Templates(directory="templates")

templates = Jinja2Templates(directory=os.path.abspath(os.path.dirname(__file__)))

@app.get("/", response_class=HTMLResponse)
async def render_html(request: Request):
    return templates.TemplateResponse("design.html", {"request": request})


@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info({"message":"connection open"})
    try:
        while True:
            logger.info({"message":"Ready to receive text"})
            data = await websocket.receive_text()
            logger.info({'message':"text received","text":data})
            ai_reponse = get_gemini_reponse(data)
            logger.info({'message':"response received","text":ai_reponse})
            await websocket.send_text(f"AI:  {ai_reponse}")
    except Exception as e:
        logger.info({'message':"Exception received","text":str(e)})

        print(e)
        print("Client disconnected.")
