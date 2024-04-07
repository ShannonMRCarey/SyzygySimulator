# SyzygySimulator
Simulator for the social deception game Syzygy

## How the Game Works
The overall success or failure of the game is determined by the number of points each system of your ship has at the end of 30 minutes. The ship has four main systems, each of which can be damaged by events and actions in the game, and each of which will be repaired by completing system-specific challenges. If any system has below zero points, at the end of the time limit, the team loses and the saboteur wins. 

Syzygy’s gameplay is divided five rounds, which each consist of two phases: planning and execution.
### Planning
In the planning phase, players receive information about a trial their ship is experiencing and are prompted to vote on a decision on how to proceed. These missions offer two different resolutions which put stresses on different ship systems, requiring the team to complete different challenges. Each mission will decrement an unknown number of points to the system selected.
Once the party has selected a mission, they need to divide themselves up amongst the challenges they choose to participate in. Each challenge requires a minimum of two team members to participate.

### Execution
Each player’s participation in a given challenge room earns one point towards the system associated with that room, if the team can complete the challenge within the time limit. To participate in a room, each player must “tap in” (scan their wristlet) at the private entry station by the door. Upon tapping in, each player is presented with a choice.
The saboteur’s choice is between sabotaging and not sabotaging the room. If they choose to sabotage the room, all points gained from this room will be flipped to the negative.
Everyone but the saboteur chooses whether to flip or not flip their portion of the score (one point). If they choose to flip, whatever outcome their score would have had (negative or positive) is reversed.

## How we Implement the Game
The Syzygy Game class maintains information about a single game's status, and runs each of its 5 rounds. Each round consists of:
1. SELECT A MISSION
2. DEDUCT POINTS FOR MISSION
3. DETERMINE ROOM ASSIGNMENTS
4. SET UP CHALLENGES
5. UPDATE TRUST

### SELECT A MISSION
To select a mission, the game first randomly selects two different rooms from its possible options.
