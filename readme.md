# Run the game
After legally obtaining a GBC file, place it in the root directory of the repo with the name `red.gbc`

# Goals
Build an AI agent which can beat Pokemon Red - the way a human would, by just looking at the screen and taking actions. Not by having some massive prior knowledge about the game.

# Play the Game Manually
Play the game with keyboard controls:
```bash
python main.py rom --manual red.gbc
```

# Run the Game with the AI Agent (Locally)

Run with Ollama agent (default):
```bash
python main.py rom red.gbc
```

Run with HuggingFace agent:
```bash
python main.py rom red.gbc --agent huggingface
```

Run in headless mode (no GUI):
```bash
python main.py rom red.gbc --headless
```

# Run the Game with the AI Agent (Remotely)

## Start the Server

Set the secret key:
```bash
export AGENT_SERVER_SECRET_KEY=your_secret_key
```

Start server with HuggingFace agent:
```bash
python server.py --agent huggingface --port 8080 --host 0.0.0.0
```

## Connect Client

Connect to remote server:
```bash
python main.py rom red.gbc --remote http://server:8080 --secret-key your_secret_key
```