# Goals
I sort of think that if we had a way to encode the game state, then a smart enough LLM could reason about the game state, and choose reasonable actions. 

The game breaks into a couple of different modes.

1. Overworld
2. Battle
3. Inventory Screens
4. Dialogues
5. Cutscenes

Choosing a reasonable action sort of depends on what state we are in, lets think about how we can encode each of the different states as text which the LLM can reason about.

## Overworld
The overworld is a grid of tiles. On one of the those tiles is a player, the play can move around the grid, and there are  objects within the grid, some of these objects are interactable, and some are not. Some are conditionally interactable, based on the player's current state. There is also a visual cone of tiles which represents the player's field of view which shifts as the player moves.

### Interactable Objects
Hidden Machine (HM) obstables are obstacles which can be interacted with based on the players current state.

NPCs are objects which can always be interacted with, some will trigger a change in mode from overworld to battle. Some will modify player inventory by gifting an item, tm, or hm, and some will simply trigger a dialogue meant to progress the story.

Portals are objects which can be interacted with, and will shift the player to a new map location. These can be doors, warp pads, ladders, etc.

### Non-Interactable Objects
Non interactable objects are objects which do not change based on the game state. These are most trees, bushes, rocks, dividers. They are largely used to keep the player within a certain bounds.

## Battle
Battles are an entirely different mode of the game. They are turn based, where a player can select to either use a move, use an item, or switch a pokemon.

### Moves
Moves are a list of up to 4 actions which a pokemon can take. Each move has a type, power, accuracy, category, and effect. All of these are taken into account, when computing the damge of a move. Once enough damage is done to a pokemon, it is knocked out of battle. The objective of the battle is to knock out all of the opponents pokemon.

### Items
Items can be used in battle to either heal your pokemon, or buff them to deal more damage. They can be used on any pokemon in your party, the pokemon actively in combat, or the pokemon on the bench.

### Switching
Pokemon encodes the notion of "active" and "bench". The active pokemon is the pokemon currently in combat able to inflict damage. The bench is the pokemon which are not currently in combat.

## Inventory Screens
While in the overworld, the player can access their inventory by pressing "start". Once the inventory has been opened, the player can select from a list of options (options, pokemon, pokedex, bag, etc).

## Dialogues
When interacting with an object, a player will transition into dialogue mode. While in dialogue mode the player cannot move, they can only read dialogue or select from a list of options, until the dialogue is complete.

## Cutscenes
Cutscenes are a series of dialogue and cinematic frames which are played to progress the story. They are not interactable, and the player must wait for them to complete.

# Game State
So when we encode game state, we want to encode, the mode we are in and the options which are available to the player in that state. For means of convience if there is only one option currently availabe,
we should just auto-select that option, there is nothing to be gained by asking the llm to reason about it. Now lets think about how we want to encode each of these different kinds of game states.

## Overworld
Some of the encoding comes naively. We could have a simple grid with some naive encodings
- w: "can walk on this tile"
- i: "can interact with this tile"
- n: "cannot interact with this tile"
- p: "player is on this tile"
```
nnwwwwnnn
nnwwwinnn
nnwwwwnnn
nnwpwwnnn
nnwwwwnnn
nnwwwwnnn
```

But already we have a few interesting decisions
- field of view: we could choose to encode the entire map as the AI's field of view, or we could find a way to encode some "memory" of where the AI has been, and what it can see.
- player position: I think that if the player is facing left and we press up, we won't move up, we will instead face up, so in some cases, we need to press up twice to move up one tile.

I guess for the field of view thing, we can try and simulate a really simple version of this directly in the chat and see how the llm can handle attention across longer sequences.