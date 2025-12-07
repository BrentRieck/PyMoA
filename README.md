# PyMoA

Mixture of Agents (MoA) command-line tool for Windows using local Ollama models and You.com search.

## Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) running locally
- You.com API key (set `YOU_COM_API_KEY` in a `.env` file)

Install dependencies:
```bash
pip install -r requirements.txt
```

Copy the environment template and add your key:
```bash
cp .env.example .env
```

Run the CLI:
```bash
python main.py "Your question here" --ollama-url http://localhost:11434
```
