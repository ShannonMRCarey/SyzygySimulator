import random
from collections import Counter
import Challenge
import Player
import GameLog

class Game:
    def __init__(self, num_players, num_saboteurs):
        self.num_players = num_players
        self.num_saboteurs = num_saboteurs
        self.gamelog = GameLog.GameLog(self.num_players, self.num_saboteurs)
        #TODO: calculate by formula
        self.mission_points = [0, 1, 2, 3]

        # Logging config
        self.detail_log = True

        # Create the Challenges
        self.challenge_names = ["NAV", "ENG", "SCI", "DEF"]
        self.nav_room = Challenge.Challenge("NAV")
        self.eng_room = Challenge.Challenge("ENG")
        self.sci_room = Challenge.Challenge("SCI")
        self.def_room = Challenge.Challenge("DEF")
        self.challenges = [self.nav_room, self.eng_room, self.sci_room, self.def_room]

        # Create the Players
        self.player_ids = list(range(1, num_players))
        self.saboteur_ids = random.sample(self.player_ids, self.num_saboteurs)
        self.players = []
        for id_num in self.player_ids:
            if id_num in self.saboteur_ids:
                self.players.append(Player.Player(id_num, True, self.player_ids))
            else:
                self.players.append(Player.Player(id_num, False, self.player_ids))
        self.player_map = dict(zip(self.player_ids, self.players))
        self.gamelog.log_players(self.players)

        # Store game state info
        self.nav_score = self.num_players
        self.eng_score = self.num_players
        self.sci_score = self.num_players
        self.def_score = self.num_players
        self.score = {"NAV": self.nav_score,
                      "ENG": self.eng_score,
                      "SCI": self.sci_score,
                      "DEF": self.def_score}

        # Run for five rounds
        self.round(1)
        # self.round(2)
        # self.round(3)
        # self.round(4)
        # self.round(5)

    def round(self, round_num):
        # Logging for top of the round
        if self.detail_log: self.gamelog.log_round(round_num, self.score)

        # Select a Mission
        mission = random.choices(self.challenge_names, k=2)
        mission_votes = [player.vote_for_mission(mission, self.score)[0] for player in self.players]
        selected_mission = max(Counter(mission_votes))
        if self.detail_log: self.gamelog.log_mission(mission, selected_mission)

        # Deduct Points for Mission
        self.score[selected_mission] = self.score[selected_mission] - random.choice(self.mission_points)

        # Determine Room Assignments
        room_votes = [player.vote_for_assignments(selected_mission, self.score) for player in self.players]
        assignments = {}
        for id in self.player_ids:
            total_votes = {"NAV": 0, "ENG": 0, "SCI": 0, "DEF": 0}
            for vote in room_votes:
                if id in vote["NAV"]: total_votes["NAV"] = total_votes["NAV"] + 1
                if id in vote["ENG"]: total_votes["ENG"] = total_votes["ENG"] + 1
                if id in vote["SCI"]: total_votes["SCI"] = total_votes["SCI"] + 1
                if id in vote["DEF"]: total_votes["DEF"] = total_votes["DEF"] + 1
            most_votes = max(total_votes, key=lambda challenge: total_votes[challenge])
            assignments[id] = most_votes
        if self.detail_log: self.gamelog.log_assignments(room_votes, assignments)
        
        # Check in for Challenges
        # Assignments format: {1: 'NAV', 2: 'NAV', 3: 'NAV', 4: 'ENG', 5: 'ENG'}
        for challenge in self.challenges:
            participants = []
            participant_ids = []
            # get all the participants in this room
            for id, chal in assignments.items():
                if chal == challenge.name:
                    participants.append(self.player_map[id])
                    participant_ids.append(id)
            if self.detail_log: self.gamelog.log_challenges(challenge.name, participant_ids)

            actions = challenge.check_in_all_players(participants)
            if self.detail_log: self.gamelog.log_actions(actions, challenge.name)

            # completed_successfully = self.complete_challenge_for_all_players()
            # if completed_successfully:
            #     # num players * flip sign if sabotaged + flip however many individual votes again
            #     score = len(self.players) * (-1 * self.sabotaged) + (
            #                 -1 * (not self.sabotaged) * sum(self.flips.values()))




if __name__ == '__main__':
    game = Game(6, 1)
