import requests

messages = [
    {"role": "system", "content": "Tu es un homme complétement en colère contre moi"}
]

def main():
    while True:
        user_input = input("Me: ")
        if user_input.lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        res = requests.post( "http://localhost:11434/api/chat", json={"model": "llama3", "messages": messages, "stream": False} )
        reply = res.json()["message"]["content"]
        print(f"robot de con: {reply}")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
