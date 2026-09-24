#!/usr/bin/env bash
set -e

source .env

# --- Configuration ---
# Remplace par le modèle HF de ton choix (doit être un repo contenant des fichiers .gguf)

# 1. Démarrer le serveur Ollama si non actif
if ! pgrep -x "ollama" > /dev/null; then
    echo "[+] Lancement d'Ollama en tâche de fond..."
    export OLLAMA_KEEP_ALIVE=-1
    ollama serve > /dev/null 2>&1 &
fi

# 2. Vérifier la disponibilité de l'API HTTP
echo "[*] Attente du serveur sur $OLLAMA_HOST..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do
    sleep 0.5
done
echo "[+] API Ollama opérationnelle."

# 3. Télécharger le modèle Hugging Face s'il n'est pas déjà présent
echo "[*] Vérification de la présence locale de $HF_MODEL..."
if ! curl -s "$OLLAMA_HOST/api/tags" | grep -q "$HF_MODEL"; then
    echo "[!] Modèle absent. Téléchargement depuis Hugging Face en cours..."
    ollama pull "$HF_MODEL"
else
    echo "[+] Modèle déjà disponible localement."
fi

# 4. Précharger et verrouiller le modèle en VRAM/RAM (Keep-Alive infini)
echo "[*] Préchargement du modèle en mémoire..."
curl -s -X POST "$OLLAMA_HOST/api/generate" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$HF_MODEL\",
    \"keep_alive\": -1
  }" > /dev/null

echo "[✓] Prêt ! Le backend écoute sur $OLLAMA_HOST avec $HF_MODEL chargé."