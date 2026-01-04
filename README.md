# AIIN
[![Watch my youtube video]((https://techcrunch.com/wp-content/uploads/2013/03/youtube-logo.jpg?w=1024))](https://deepwiki.com/y3chnx/AIIN/tree/main)

AIIN is an open-source web browser featuring a built-in AI assistant that runs entirely on your local machine. It combines a standard tabbed browsing experience with the power of a large language model for assistance, search, and conversation.

## Features

*   **Local AI:** The integrated AI assistant runs on a local LLM, ensuring privacy and offline capability. No data is sent to external servers.
*   **Conversational Interface:** Start a conversation with the AI from the new tab page or interact with it in a dedicated chat view.
*   **Modern Web Browser:** A tabbed browser built with PyQt and QtWebEngine, including essential controls like back, forward, reload, and a URL bar.
*   **Download Manager:** A simple interface to track and access your downloaded files.
*   **Cross-Platform:** Built with Python and PyQt5, allowing it to run on various operating systems.

## Architecture

The application consists of two main components that run concurrently:

1.  **Browser Frontend (`web.py`):** A desktop application built using PyQt5. It provides the main browser window, tab management, and web page rendering via `QWebEngineView`.
2.  **AI Backend (`ai_engine.py`):** A lightweight Flask server that runs in the background. It exposes an `/ask` API endpoint. When the user sends a message in the chat UI, the frontend makes a request to this local server. The server then uses `llama-cpp-python` to process the prompt with the local LLM and returns the generated response.

The New Tab and Chat pages (`new.html`, `new2.html`) are local HTML files loaded into the browser that use JavaScript's `fetch` API to communicate with the AI backend.

## Getting Started

Follow these instructions to set up and run the AIIN browser on your local machine.

### Prerequisites

*   Python 3.8+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/y3chnx/aiin.git
    cd aiin
    ```

2.  **Download the Language Model:**
    The AI assistant requires a model file in GGUF format. Download the recommended model from the link below and place it in the designated folder.

    *   **URL:** [mistral-7b-instruct-v0.2.Q4_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf)
    *   **Destination:** Create a `model/models/` directory and save the file as `model/models/model.gguf`.

3.  **Install Dependencies:**
    Install the required Python packages from `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```
    > **Note:** The `llama-cpp-python` package compiles the model bindings. Depending on your system (NVIDIA GPU, Apple Metal), you may want to install it with specific flags for hardware acceleration to improve performance. Please refer to the official [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) documentation for advanced installation options.

### Running the Application

Once the setup is complete, run the main `web.py` script to launch the browser.

```bash
python web.py
```

The script will first start the local Flask server for the AI and then launch the browser GUI.

## Usage

*   **Start a Conversation:** On the "New Tab" page, type your question into the search bar and press `Enter` or click the search icon. This will navigate you to the chat interface with the AI's response.
*   **Web Browsing:** Use the URL bar to navigate to any website. You can open new tabs using the `+` button and manage them as you would in a standard browser.
*   **Chat with the AI:** In the chat view, you can have an ongoing conversation with the AIIN assistant. The chat history is maintained for the current session.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
