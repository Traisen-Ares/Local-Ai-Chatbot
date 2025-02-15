# Local-Ai-Chatbot
A simple lightweight AI chatbot that runs locally on your own system

Welcome to this simple local AI chatbot.

In order to make it work please visit "https://ollama.com/" and download Ollama.
Then open your terminal and check if ollama is running with the command "ollama"
Now you can download the model, this app is made to run on Llama3 so in the terminal type "ollama pull llama3"

If you want to switch the model type "ollama pull {model name}"
In main.py change the model name in: "model = OllamaLLM(model="{your new model name}", temperature=2, top_p=5)" 
