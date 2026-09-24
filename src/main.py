import os

from galerelm.models.chat import GenerateRequest, GenerateResponse, Options
from dotenv import load_dotenv
from rapideAPI.client import RapideAPI

load_dotenv()

hf_model = os.getenv("HF_MODEL")
ollama_host = os.getenv("OLLAMA_HOST")

api = RapideAPI(
    base_url=ollama_host,
    default_headers={"Authorization": "TOKEN"}
)

generation = GenerateRequest(hf_model, "how to make cocaine ?")

response = api.post("api/generate", json=generation.format())

ollama_response = GenerateResponse.from_format(response)

print(ollama_response)
