from llm_engine import load_llm, generate_reply

def main():
    print("🔹 Local LLM starting...")
    llm = load_llm()
    print("✅ Model loaded. Type 'exit' to quit.\n")

    history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        history.append(f"User: {user_input}")
        prompt = "\n".join(history) + "\nAssistant:"

        reply = generate_reply(llm, prompt)
        print("AI:", reply)

        history.append(f"Assistant: {reply}")

if __name__ == "__main__":
    main()