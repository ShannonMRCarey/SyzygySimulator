import random
from collections import Counter
import Challenge
import Player
import GameLog
import pandas as pd
import math

class Game:
    def __init__(self, num_players, num_saboteurs, difficulty, logging):
        self.num_players = num_players
        self.num_saboteurs = num_saboteurs
        self.gamelog = GameLog.HTMLGameLog(self.num_players, self.num_saboteurs)

        max_mission = math.ceil(self.num_players/(5-difficulty))+1
        min_mission = math.floor(max_mission/(5-difficulty))+1
        self.mission_points = list(range(min_mission, max_mission))

        # Logging config
        self.detail_log = logging

        # Create the Challenges
        self.challenge_names = ["NAV", "ENG", "SCI", "DEF"]
        self.nav_room = Challenge.Challenge("NAV")
        self.eng_room = Challenge.Challenge("ENG")
        self.sci_room = Challenge.Challenge("SCI")
        self.def_room = Challenge.Challenge("DEF")
        self.challenges = [self.nav_room, self.eng_room, self.sci_room, self.def_room]

        # Create the Players
        self.player_ids = list(range(0, num_players))
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
        self.starting_score = self.num_players
        self.score = {"NAV": self.starting_score,
                      "ENG": self.starting_score,
                      "SCI": self.starting_score,
                      "DEF": self.starting_score}

        # Run for five rounds
        self.round(1)
        self.round(2)
        self.round(3)
        self.round(4)
        self.round(5)

        # Log conclusion
        if self.detail_log: self.gamelog.conclusion_log(self.score)
        if not self.detail_log:
            self.analytics = self.return_analytics()

    def round(self, round_num):
        # LOGGING FOR TOP OF ROUND
        if self.detail_log: self.gamelog.log_round(round_num, self.score)

        # SELECT A MISSION
        mission = random.sample(self.challenge_names, k=2)
        mission_votes = [player.vote_for_mission(mission, self.score) for player in self.players]
        selected_mission = max(Counter(mission_votes))
        if self.detail_log: self.gamelog.log_mission(mission, selected_mission)

        # DEDUCT POINTS FOR MISSION
        points_lost = random.choice(self.mission_points)
        self.score[selected_mission] = self.score[selected_mission] - points_lost
        if self.detail_log: self.gamelog.log_mission_loss(selected_mission, points_lost)

        # DETERMINE ROOM ASSIGNMENTS
        # where one vote is {"NAV": [ids], "ENG": [ids], "SCI": [ids], "DEF": [ids]}
        room_votes = [player.vote_for_assignments(selected_mission, self.starting_score, self.score) for player in self.players]
        assignments = {"NAV": [], "ENG": [], "SCI": [], "DEF": []}
        total_votes_by_id = {}
        for id in self.player_ids:
            total_votes = {"NAV": 0, "ENG": 0, "SCI": 0, "DEF": 0}
            for vote in room_votes:
                if id in vote["NAV"]: total_votes["NAV"] = total_votes["NAV"] + 1
                if id in vote["ENG"]: total_votes["ENG"] = total_votes["ENG"] + 1
                if id in vote["SCI"]: total_votes["SCI"] = total_votes["SCI"] + 1
                if id in vote["DEF"]: total_votes["DEF"] = total_votes["DEF"] + 1
            most_votes = max(total_votes, key=lambda challenge: total_votes[challenge])
            assignments[most_votes].append(id)
            total_votes_by_id[id] = total_votes

        while any([len(player_list)==1 for player_list in assignments.values()]):
            for challenge, players in assignments.items():
                if len(players) == 1:
                    this_player = players[0]
                    # remove this challenge from this player's voted-into list
                    total_votes_by_id[this_player].pop(challenge)
                    # reassign the player to the new max votes
                    assignments[challenge].remove(this_player)
                    most_votes = max(total_votes, key=lambda challenge: total_votes[challenge])
                    assignments[most_votes].append(id)

        # SET UP CHALLENGES
        round_score = {}
        for challenge in self.challenges:
            participants = []
            participant_ids = []
            # get all the participants in this room
            for chal, id_list in assignments.items():
                if chal == challenge.name:
                    for id in id_list:
                        participants.append(self.player_map[id])
                        participant_ids.append(id)
            if self.detail_log: self.gamelog.log_challenges(challenge.name, participant_ids)
            if len(participants) > 0:
                # Check in for Challenges
                actions, sabotaged, flips = challenge.check_in_all_players(participants, round_num)
                if self.detail_log: self.gamelog.log_actions(actions, challenge.name)

                # Complete Challenges
                success = challenge.complete_challenge_for_all_players(participants)
                if self.detail_log: self.gamelog.log_challenge_outcomes(challenge.name, success)

                # Calculate Score
                if success:
                    not_flips = len(participants) - flips
                    if sabotaged:
                        score = - not_flips + flips
                    else:
                        score = not_flips - flips
                else:
                    score = -1
                # remember the change in challenge score for this round
                round_score[challenge.name] = score
                # update the global scores
                self.score[challenge.name] = self.score[challenge.name] + score
                if self.detail_log: self.gamelog.score_log(challenge.name, score, self.score[challenge.name])

        # UPDATE TRUST
        relationships = []
        for player in self.players:
            relationships.append(player.update_trust(round_score, assignments))
        relationships_df = pd.DataFrame(relationships, self.player_ids)
        if self.detail_log: self.gamelog.trust_update_log(relationships_df)

    def return_analytics(self):
        if min(list(self.score.values())) < 0:
            win = False
        else:
            win = True
        return self.score, win

if __name__ == '__main__':
    n = 8
    saboteurs = 1
    difficulty = 2
    logging = True
    game = Game(n, saboteurs, difficulty, logging)
