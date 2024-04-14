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
Each player is asked which mission they would like to vote for. The Player method vote_for_mission will always return the mission with the highest score.

### DEDUCT POINTS FOR MISSION
Each mission will lose the team between 1 and 3 points.

### DETERMINE ROOM ASSIGNMENTS
To determine where players will go, the game first asks players to vote_for_assignments.
In a real syzygy game, this voting mechanism would be replaced by informal discussion of where team members should go.
To simulate this, each player submits votes to the game, which then selects the most-agreed-upon situation.

in vote_for_assignment, each player considers each challenge room in order of importance (the one with the lowest point score).
They will try to put the people they trust most, in order, into the rooms they care about most. To determine how many 
players they want in each room, they select the arrangement which yields the highest expected score. For example, if 
there are six players, and their normalized relationship matrix with them is [0.4,0.25, 0.2, 0.5, 0.5, 0.05],
they weigh if putting the first two in a room together (0.4*0.24* 2 points earned) would be better than putting the first three 
together (0.4*0.24*0.2* 3 points earned) and so on.

Once the game has all votes in, it identifies which room each player received the most votes for, and assigns them. In
the case that one player would be assigned alone to a room, the game will pick the second most popular choice for them,
and so on.

### SET UP CHALLENGES
Set up challenges includes both the challenge check-in and the actual execution. check_in_for_challenge asks each player
to evaluate the chances of success in their own room, which is based off the chances of there being a saboteur in their
room statistically, and the trust they have of each other person in the room.

Challenge execution is simulated here using each player's skill level in that challenge as a weight for the chances of
them succeeding/failing. The Game sets a threshold for what constitutes overall success or failure.

### UPDATE TRUST
The score from each room for each round is used to help players determine who to flip on in the future, and who to
trust. If a player was in a room which lost points, everyone else trusts them less, proportionate to how much they
trusted them before and how many people were in the room that scored negatively. The inverse is true of a player
in a room who gained points. The one additional consideration made is that when a player evaluates their own room,
they remove themselves from the trust update (eg. if they and one other person were in a room that failed, since
they know they're good, they entirely blame the other person for the failure).
