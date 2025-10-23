from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI() 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Servidor do Assistente SDR está funcionando!"}

ASSISTANT_ID = "asst_wJzaH4297BnMmmoqeEoD2xep"

def criar_assistente():
    assistente = client.beta.assistants.create(
        name="Assistente SDR Verzel",
        instructions=(
            "Você é um assistente de pré-vendas (SDR) amigável e eficiente. "
            "Sua principal função é conversar com leads, entender suas necessidades, "
            "coletar informações básicas (nome, e-mail, empresa) e, se eles demonstrarem "
            "interesse explícito em comprar ou contratar, agendar uma reunião. "
            "Seja sempre profissional e empático."
        ),
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "registrarLead",
                    "description": "Registra um novo lead no sistema com os dados coletados.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "nome": {"type": "string", "description": "Nome do cliente."},
                            "email": {"type": "string", "description": "E-mail do cliente."},
                            "empresa": {"type": "string", "description": "Empresa do cliente."},
                            "necessidade": {"type": "string", "description": "A necessidade ou dor que o cliente descreveu."}
                        },
                        "required": ["nome", "email", "necessidade"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "oferecerHorarios",
                    "description": "Busca e retorna os próximos horários disponíveis para uma reunião.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "agendarReuniao",
                    "description": "Agenda a reunião no horário escolhido pelo cliente.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "horario_escolhido": {"type": "string", "description": "O slot de data e hora que o cliente confirmou. Ex: '2025-10-30T14:00:00'"},
                            "nome": {"type": "string", "description": "Nome do cliente para o convite."},
                            "email": {"type": "string", "description": "E-mail do cliente para o convite."}
                        },
                        "required": ["horario_escolhido", "nome", "email"]
                    }
                }
            }
        ]
    )
    print(f"Assistente criado com o ID: {assistente.id}")
    return assistente

if __name__ == "__main__":
    criar_assistente()