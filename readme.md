# Run the game
After legally obtaining a GBC file, place it in the root directory of the repo with the name `red.gbc`

# Goals
Build an AI agent which can beat Pokemon Red - the way a human would, by just looking at the screen and taking actions. Not by having some massive prior knowledge about the game.

# Current Status
- [x] Naively connected a vllm (llama 3.2 llb) to a gameboy emulator, prompting the model to "choose" an action. Was not better than random.
- [ ] Belief is that model cannot see what is going on, thus cannot reason. Thus building a couple simple text based enviroments, which mirror some of the complexity of pokemon, to see how the model does.