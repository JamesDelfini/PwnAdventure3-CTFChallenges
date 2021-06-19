## Game Structure
Information
- Game: PwnAdventure 3
- Genre: MMORPG - Team Adventure Quest
- Developer: Vector35
- Game Engine: Unity (cross-platform)
- RE Complexity: Medium(no obfuscation, no signature/encryption, all-in-on logic file)

Client/Servers
- Master Game Server - Login, team, characters, assign intance
- Game Server - Game Instances
- Client


Application Layer:
- Loading the game
- Receiving user inputs
- File/memory management
- Network Communication

Game Logic
- Events (if player kill/pick up/..., then ...)
- States and data (items, NPC, enemy, player quests, etc)
- Physics (gravity, hit box, movement collision with wall, etc)

Game View:
- Graphic engine
- Audio

Offline Game:
- All files and executions are done locally
- Full control over the game
- Obfuscation/anti-RE is the only obstacle

Online Game:
- Client game logic
- Server game logic
- Bi-directional network communication
- Unknown logic on server side
- Uncontrolled logic on server side

## Define Target
Top Down Approach
1. Play the game to identify what is valuable:
- Items (coins, weapons, spells, etc)
- State (quest unlocked, being level 42, etc)
- Increase specs (damage x10, health +1000, etc)
- Enchance capabilities (run faster, see through wall, jump higher, etc)
Identify where it is used, then reverse and exploit

Bottom-up approach
1. Reverse the binary/network to identify potential weakness

Targets for this workshop:
- Spawn wherever we want
- Pick up remote items
- Find secret to unlock quest
- Find vulnerability to kill boss
- Run faster
- Jump higher
- Teleport anywhere

Where to look?
- Network communication (if online)
- Local saved data
- Client game logic binary
- Server game logic binary (if online)
- Rendering engine

What to do?
- RE network protocol
- Edit local saved data
- RE game logic
- Patch binary/Hook libraries
- Edit rendering engine
- Build bots (automate task to be faster and more accurate)
