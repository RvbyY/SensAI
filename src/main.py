import os

from galerelm.models.chat import GenerateRequest, GenerateResponse, Options
from dotenv import load_dotenv
from rapideAPI.client import RapideAPI
import logging

# Configure les logs pour tout afficher dans la console avec un beau format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

load_dotenv()

hf_model = os.getenv("HF_MODEL")
ollama_host = os.getenv("OLLAMA_HOST")

api = RapideAPI(
    base_url=ollama_host,
    default_headers={"Authorization": "TOKEN"}
)

user_prompt = input("\nPosez votre question au modèle : ")

# IMPORTANT: On met stream=False pour qu'Ollama renvoie un seul JSON complet, 
# sinon il renvoie un flux de texte (plusieurs JSON bout à bout) et le parseur échoue
generation = GenerateRequest(model=hf_model, prompt=user_prompt, stream=False)

response = api.post("api/generate", json=generation.format())

# Sécurité: si RapideAPI a renvoyé une string (ex: JSON mal formé), on utilise from_json
if isinstance(response, str):
    ollama_response = GenerateResponse.from_json(response)
else:
    ollama_response = GenerateResponse.from_format(response)

print("\n--- RÉPONSE DU MODÈLE ---")
if ollama_response:
    print(ollama_response.response)
else:
    print("Erreur: Impossible de lire la réponse.")
