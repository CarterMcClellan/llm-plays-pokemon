# Making the action handler less bad.

1. Right now we show that there are 2 pokemon in the party when I only have 1. The second pokemon is level 0 type ID 255, which is the same it showed when I had no pokemon in the party. Eg.
```
Party Pokemon:
  Pokemon 1: Level 6, HP 100.0%, Type ID 176
  Pokemon 2: Level 0, HP 0.0%, Type ID 255
```

2. Would be cool if in battle we could see the names of my pokemon, the names of their pokemon, everyones respective pp, etc...

i think that this is all a part of the party_struct