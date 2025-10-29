import os
import requests
import json

PIPEFY_API_URL = "https://api.pipefy.com/graphql"

def criar_ou_atualizar_lead(nome: str, email: str, empresa: str, necessidade: str):
    """
    Cria um card no Pipefy e depois o atualiza com os detalhes do lead.
    """
    pipefy_api_key = os.getenv("PIPEFY_API_KEY")
    pipefy_pipe_id = os.getenv("PIPEFY_PIPE_ID")

    if not pipefy_api_key or not pipefy_pipe_id:
        print("ERRO: As variáveis PIPEFY_API_KEY ou PIPEFY_PIPE_ID não foram encontradas.")
        return "Erro de configuração no servidor."

    headers = {
        "Authorization": f"Bearer {pipefy_api_key}",
        "Content-Type": "application/json",
    }

    print(f"--- Serviço Pipefy: Criando card para o lead {nome} ---")
    
    create_mutation_query = f"""
    mutation {{
      createCard(input: {{
        pipe_id: "{pipefy_pipe_id}",
        title: "Lead - {nome}"
      }}) {{
        card {{
          id
        }}
      }}
    }}
    """
    
    try:
        response = requests.post(
            PIPEFY_API_URL, headers=headers, data=json.dumps({"query": create_mutation_query})
        )
        response.raise_for_status()
        response_data = response.json()

        if "errors" in response_data:
            print(f"Erro da API do Pipefy ao criar o card: {response_data['errors']}")
            return "Ocorreu um erro ao registrar o lead (fase 1)."

        card_id = response_data['data']['createCard']['card']['id']
        print(f"Card criado com sucesso. ID: {card_id}")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API do Pipefy: {e}")
        return "Não foi possível conectar ao CRM para registrar o lead."

    print(f"--- Serviço Pipefy: Atualizando card {card_id} com os detalhes ---")

    update_mutation_query = f"""
    mutation {{
      updateFieldsValues(input: {{
        nodeId: "{card_id}",
        values: [
          {{ fieldId: "neg_cio", value: "{nome}" }},
          {{ fieldId: "email_profissional", value: "{email}" }},
          {{ fieldId: "empresa", value: "{empresa}" }},
          {{ fieldId: "necessidade_dor", value: "{necessidade}" }},
          {{ fieldId: "interesse_confirmado", value: "Sim" }}
        ]
      }}) {{
        clientMutationId
      }}
    }}
    """

    try:
        response = requests.post(
            PIPEFY_API_URL, headers=headers, data=json.dumps({"query": update_mutation_query})
        )
        response.raise_for_status()
        response_data = response.json()

        if "errors" in response_data:
            print(f"Erro da API do Pipefy ao atualizar o card: {response_data['errors']}")
            return "Ocorreu um erro ao registrar o lead (fase 2)."

        print(f"Card {card_id} atualizado com sucesso com todos os detalhes.")
        return f"Lead para '{nome}' foi registrado com sucesso no CRM."

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API do Pipefy (fase 2): {e}")
        return "Não foi possível conectar ao CRM para atualizar o lead."