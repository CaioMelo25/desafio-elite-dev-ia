import os
import requests
from datetime import datetime, timedelta, timezone
import locale
import json

# Configura o locale para português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR não encontrado, usando o padrão.")

CALENDLY_API_URL = "https://api.calendly.com"

def format_datetime_for_calendly(dt_obj):
    return dt_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def buscar_horarios_disponiveis():
    print("--- Serviço Agenda: Buscando horários disponíveis no Calendly... ---")
    
    # Carrega as variáveis de ambiente dentro da função
    calendly_api_key = os.getenv("CALENDLY_API_KEY")
    calendly_event_type_uri = os.getenv("CALENDLY_EVENT_TYPE_URI")

    if not calendly_event_type_uri or not calendly_api_key:
        return "Erro: O URI do tipo de evento do Calendly não está configurado."

    headers = {"Authorization": f"Bearer {calendly_api_key}", "Content-Type": "application/json"}
    
    start_time_obj = datetime.now(timezone.utc) + timedelta(minutes=5)
    end_time_obj = start_time_obj + timedelta(days=7)
    start_time = format_datetime_for_calendly(start_time_obj)
    end_time = format_datetime_for_calendly(end_time_obj)

    api_endpoint = f"{CALENDLY_API_URL}/event_type_available_times"
    params = {"event_type": calendly_event_type_uri, "start_time": start_time, "end_time": end_time}

    try:
        response = requests.get(api_endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        available_times = data.get("collection", [])
        if not available_times:
            return "Não encontrei horários disponíveis nos próximos 7 dias."

        horarios_formatados = []
        for time in available_times[:3]:
            start_time_str = time.get("start_time")
            dt_obj_utc = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            dt_obj_brt = dt_obj_utc.astimezone(timezone(timedelta(hours=-3)))
            horarios_formatados.append(dt_obj_brt.strftime("%d de %B às %H:%M"))
        
        return f"Claro! Encontrei os seguintes horários disponíveis: {', '.join(horarios_formatados)}."
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com a API do Calendly: {e}")
        return "Desculpe, não consegui verificar os horários disponíveis no momento."

def agendar_reuniao_calendly(horario_escolhido: str, nome: str, email: str):
    print(f"--- Serviço Agenda: Gerando link de agendamento para {nome} ---")
    
    # Carrega as variáveis de ambiente dentro da função
    calendly_api_key = os.getenv("CALENDLY_API_KEY")
    calendly_event_type_uri = os.getenv("CALENDLY_EVENT_TYPE_URI")

    if not calendly_event_type_uri or not calendly_api_key:
        return "Erro: O URI do tipo de evento do Calendly não está configurado."

    headers = {"Authorization": f"Bearer {calendly_api_key}", "Content-Type": "application/json"}
    
    api_endpoint = f"{CALENDLY_API_URL}/scheduling_links"
    payload = {
        "max_event_count": 1,
        "owner": calendly_event_type_uri,
        "owner_type": "EventType"
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        booking_url = data.get("resource", {}).get("booking_url")
        if not booking_url:
            return "Não consegui gerar o link de agendamento, por favor, tente novamente."

        print(f"Link de agendamento gerado: {booking_url}")
        return f"Perfeito! Aqui está o seu link exclusivo para confirmar a reunião: {booking_url}. Basta clicar para finalizar o agendamento."
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar link de agendamento no Calendly: {e}")
        return "Desculpe, não consegui gerar o link de agendamento no momento."