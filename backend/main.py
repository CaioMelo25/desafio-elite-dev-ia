import os
import time
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI, BadRequestError
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pipefy_service import criar_ou_atualizar_lead
from agenda_service import buscar_horarios_disponiveis, agendar_reuniao_calendly

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
client = OpenAI()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSISTANT_ID = "asst_wJzaH4297BnMmmoqeEoD2xep"

def registrarLead(nome: str, email: str, empresa: str, necessidade: str):
    return criar_ou_atualizar_lead(nome, email, empresa, necessidade)

def agendarReuniao(horario_escolhido: str, nome: str, email: str):
    return agendar_reuniao_calendly(horario_escolhido, nome, email)

available_tools = {
    "registrarLead": registrarLead,
    "oferecerHorarios": buscar_horarios_disponiveis,
    "agendarReuniao": agendarReuniao,
}

@app.get("/")
def read_root():
    return {"message": "Servidor do Assistente SDR está funcionando"}

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None

@app.post("/chat")
def handle_chat(request: ChatRequest):
    thread_id = request.thread_id
    user_message = request.message

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id

    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )
    except BadRequestError as e:
        if "while a run" in str(e) and "is active" in str(e):
            logging.warning(f"Thread presa detectada ({thread_id}). Iniciando uma nova conversa.")
            thread = client.beta.threads.create()
            thread_id = thread.id
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_message
            )
        else:
            logging.error(f"Erro inesperado do BadRequest ao adicionar mensagem: {e}")
            raise e

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    while run.status in ['queued', 'in_progress', 'requires_action']:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        
        if run.status == "requires_action":
            logging.info("Assistente solicitou a execução de uma ferramenta.")
            tool_outputs = []
            
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                output = None

                if tool_name in available_tools:
                    tool_function = available_tools[tool_name]
                    output = tool_function(**tool_args)

                    if output:
                        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
            
            if tool_outputs:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        time.sleep(1)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        response = messages.data[0].content[0].text.value
        return {"response": response, "thread_id": thread_id}
    else:
        error_details = run.last_error
        logging.error(f"A execução da IA falhou com status '{run.status}'. Detalhes: {error_details}")
        error_message = f"Status: {run.status}"
        if error_details: error_message = error_details.message
        return {"response": f"A execução falhou: {error_message}", "thread_id": thread_id}