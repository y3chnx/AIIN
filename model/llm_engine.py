import sys
from pathlib import Path
from llama_cpp import Llama

def get_base_path():
    if getattr(sys, "_MEIPASS", False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent

def load_knowledge():
    base = get_base_path()
    path = base / "knowledge.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

KNOWLEDGE = load_knowledge()

def load_llm():
    base = get_base_path()
    model_path = base / "models" / "model.gguf"

    if not model_path.exists():
        raise FileNotFoundError(model_path)

    return Llama(
        model_path=str(model_path),
        n_ctx=1024,
        n_gpu_layers=35,   
        n_threads=8,
        n_batch=512,
        verbose=False
    )

def generate_reply(llm, user_input):
    prompt = f"""
You are AIIN, an assistant built into a web browser.
Use the following information if relevant.

{KNOWLEDGE}

User: {user_input}
Assistant:
"""
    output = llm(
        prompt=prompt,
        max_tokens=256,
        temperature=0.7,
        stop=["User:"]
    )
    return output["choices"][0]["text"].strip()
