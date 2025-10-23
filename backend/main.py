import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI()

app = FastAPI()

ASSISTANT_ID = "asst_wJzaH4297BnMmmoqeEoD2xep"

@app.get("/")
def read_root():
    return {"message": "Servidor do Assistente SDR está funcionando"}

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None 

@app.post("/chat")
def handle_chat(request: ChatRequest):
    thread_id = request.thread_id
    if thread_id is None:
        thread = client.beta.threads.create()
        thread_id = thread.id

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=request.message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    while run.status in ['queued', 'in_progress']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value
        return {"response": response, "thread_id": thread_id}
    else:
        return {"response": "Ocorreu um erro ou uma ação é necessária.", "thread_id": thread_id, "status": run.status}