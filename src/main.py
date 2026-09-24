import json
import os

from galerelm.models.chat import Chat, ChatResponse, Options, Message, MessageList
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

# Valeurs par défaut cohérentes pour l'inférence d'un LLM
options = Options(
    seed=0,                
    temperature=0.7,       
    top_k=40,              
    top_p=0.9,             
    min_p=0.05,            
    stop=["\nuser:", "</s>"], 
    num_ctx=4096,          
    num_predict=512        
)

# On prépare le message utilisateur
messages = MessageList([])

# On configure le Chat (en activant le stream)
user_chat = Chat(
    model=hf_model, 
    messages=messages, 
    tools=None, 
    request_format="json",
    options=options, 
    stream=True, 
    think="medium",
    keep_alive="5m", 
    logprobs=False, 
    top_logprobs=0
)

user_chat.add_message(user_prompt, [], None)

# Lancement de la requête avec stream=True (récupère l'objet response brut de requests)
response = api.post("api/chat", json=user_chat.format(), stream=True)

# On s'assure qu'il n'y a pas eu d'erreur HTTP
response.raise_for_status()



print("\n--- RÉPONSE DU MODÈLE ---")
full_response: list[str] = []
final_chunk = None

# Parcourt chaque ligne NDJSON au fil de l'eau
for line in response.iter_lines():
    if not line:
        continue

    # Décodage de la ligne JSON
    chunk = json.loads(line.decode("utf-8"))
    
    # Extraction du morceau de réponse
    token = chunk.get("message", {}).get("content", "")
    if token:
        # Affichage direct dans le terminal
        print(token, end="", flush=True)
        full_response.append(token)

    # Signal de fin de génération (le dernier chunk contient toutes les stats)
    if chunk.get("done", False):
        print()  # Saut de ligne final
        final_chunk = chunk

# Reconstitution du texte complet
full_text = "".join(full_response)

if final_chunk:
    # On met le texte complet dans le dictionnaire du dernier chunk pour reconstruire l'objet final
    if "message" not in final_chunk:
        final_chunk["message"] = {}
    
    final_chunk["message"]["role"] = "assistant"
    final_chunk["message"]["content"] = full_text
    
    # On parse le tout directement dans un bel objet ChatResponse !
    ollama_response = ChatResponse.from_format(final_chunk)
    
    print("\n--- OBJET CHATRESPONSE SAUVEGARDÉ ---")
    print(f"Modèle: {ollama_response.model}")
    print(f"Tokens évalués: {ollama_response.eval_count}")
    print(f"Temps de génération: {ollama_response.eval_duration / 1e9:.2f} s")
else:
    print("\nErreur: Flux interrompu avant la fin.")

