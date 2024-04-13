'''
Reward:
this round's score

State:
-stat block
-game score

Action Space:
any possible allocation

'''

import math
import numpy as np

class PlayerAI:
    def __init__(self, player_ids, num_saboteurs):
        self.player_ids = player_ids
        self.num_saboteurs = num_saboteurs
        print(self.state_space())

    def state_space(self):
        l = len(self.player_ids)
        all_options = []

        # how can the rooms be allocated?

        num_possible_simultaneous_rooms = max(math.floor(l/2),4)

        # 1room
        if num_possible_simultaneous_rooms >=1:
            one_room_options = [l]
            all_options.append(one_room_options)

        # 2rooms
        if num_possible_simultaneous_rooms >= 2:
            two_room_options = []
            for a in range(2, l-1):
                room1 = l-a
                room2 = l-room1
                two_room_options.append([room1, room2])
            all_options.append(two_room_options)

        # 3rooms
        if num_possible_simultaneous_rooms >= 3:
            three_room_options = []
            for a in range(2, l-1):
                room1 = l-a
                aremainder = l-room1
                for b in range(2, aremainder-1):
                    room2 = l-room1-b
                    room3 = l-room1-room2
                    three_room_options.append([room1 , room2, room3])
            all_options.append(three_room_options)

        # 4rooms
        if num_possible_simultaneous_rooms >= 4:
            four_room_options = []
            for a in range(2, l - 1):
                room1 = l - a
                aremainder = l - room1
                for b in range(2, aremainder - 1):
                    room2 = l - room1 - b
                    bremainder = l - room1 - room2
                    for c in range (2, bremainder - 1):
                        room3 = l - room1 - room2 - c
                        room4 = l - room1 - room2 - room3
                        four_room_options.append([room1, room2, room3, room4])
            all_options.append(four_room_options)

        one_room = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        two_rooms = [[1,0,0,1],[1,0,1,0],[1,1,0,0],[0,1,0,1],[0,1,1,0],[0,0,1,1]]
        three_rooms = [[1,1,1,0],[1,1,0,1],[1,0,1,1],[0,1,1,1]]
        four_rooms = [[1,1,1,1]]

        return all_options


if __name__ == '__main__':
    playertest = PlayerAI([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1)


