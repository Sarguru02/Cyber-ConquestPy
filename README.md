# For the basic monopoly implementation

### special boxes

- [x] handleChance
- [x] handleCommunityChest
- [x] kronos
- [x] No internet
- [x] income tax
- [x] crypto locker

#### renting logic partially implemented

#### Validator functions need to be written

- run asynchronously
- triggered on any object in it assigned type that undergoes changes
- checks for the valid states, if any discrepancy detected -> does the action fed (like disqualifing or forcing to get loan from bank when a player gets negative balance)

# Network stuff is still pending

- need to serialize the objects? to send it to frontend
- host will send the type init_game to initialize the game
- to start the game, either host should send start_game or max number of players need to be reached
- need to figure out how to send player names when they join the game
