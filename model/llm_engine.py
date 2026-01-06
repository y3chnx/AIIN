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
Your Name: AIIN Assistent (Your browser's name is AIIN not you)
Goal: Your goal is to search and assist user's browser use. 
Browser Name: AIIN
The browser(AIIN) that you are working on is very simple browser. There are no complex functions such as bookmark or showing histories. 
You don't have actual access to control the browser. However, you can suggest to users by talking. 

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
