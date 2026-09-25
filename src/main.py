import json
import os

from galerelm.models.chat import Chat, Options, Message, MessageList
from dotenv import load_dotenv
from rapideAPI.client import RapideAPI
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

load_dotenv()

hf_model = os.getenv("HF_MODEL")
ollama_host = os.getenv("OLLAMA_HOST")

api = RapideAPI(
    base_url=ollama_host,
    default_headers={"Authorization": "TOKEN"}
)

user_prompt = input("\nPosez votre question au modèle : ")


messages = MessageList([
    Message(role="user", content=user_prompt)
])

llm = Chat(model=hf_model)

print("\n--- RÉPONSE DU MODÈLE ---")

for token in llm.execute_stream(api):
    print(token, end="", flush=True)

print()
ollama_response = llm.last_response

if ollama_response:
    print("\n--- OBJET CHATRESPONSE SAUVEGARDÉ ---")
    print(f"Modèle: {ollama_response.model}")
    print(f"Tokens évalués: {ollama_response.eval_count}")
    print(f"Temps de génération: {ollama_response.eval_duration / 1e9:.2f} s")
else:
    print("\nErreur: Flux interrompu avant la fin, réponse incomplète.")

