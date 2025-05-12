from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
load_dotenv()

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Welcomee to your Azure AI-powered education app!"}

@app.post("/analyze/")
def analyze_text(input: TextInput):
    # This is just a placeholder response
    return {"received_text": input.text}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)