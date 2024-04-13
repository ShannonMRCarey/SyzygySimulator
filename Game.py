import copy
import random
from collections import Counter
import Challenge
import Player
import GameLog
import pandas as pd
from statistics import mode

class Game:
    def __init__(self, num_players, num_saboteurs):
        self.num_players = num_players
        self.num_saboteurs = num_saboteurs
        self.gamelog = GameLog.HTMLGameLog(self.num_players, self.num_saboteurs)
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
        self.gamelog.conclusion_log(self.score)

    def round(self, round_num):
        # LOGGING FOR TOP OF ROUND
        if self.detail_log: self.gamelog.log_round(round_num, self.score)

        # SELECT A MISSION
        mission = random.sample(self.challenge_names, k=2)
        mission_votes = [player.vote_for_mission(mission, self.score)[0] for player in self.players]
        selected_mission = max(Counter(mission_votes))
        if self.detail_log: self.gamelog.log_mission(mission, selected_mission)

        # DEDUCT POINTS FOR MISSION
        points_lost = random.choice(self.mission_points)
        self.score[selected_mission] = self.score[selected_mission] - points_lost
        if self.detail_log: self.gamelog.log_mission_loss(selected_mission, points_lost)

        # DETERMINE ROOM ASSIGNMENTS
        # where one vote is {"NAV": [ids], "ENG": [ids], "SCI": [ids], "DEF": [ids]}
        challenge_votes = [player.vote_for_assignments(selected_mission, self.starting_score, self.score) for player in self.players]

        # use mode of votes to determine how many people should be in each room
        num_per_chal_votes = {"NAV": [], "ENG": [], "SCI": [], "DEF": []}
        for v in challenge_votes:
            for challenge, ids in v.items():
                num_per_chal_votes[challenge].append(len(ids))
        num_per_chal = {"NAV": mode(num_per_chal_votes["NAV"]),
                        "ENG": mode(num_per_chal_votes["NAV"]),
                        "SCI": mode(num_per_chal_votes["NAV"]),
                        "DEF": mode(num_per_chal_votes["NAV"])}
        # if the modes don't add up, add the remaining people to the lowest scoring room
        if sum(num_per_chal.values()) < len(self.players):
            lowest_score = min(self.score.values())
            challenge = [key for key, val in self.score.items() if val == lowest_score][0]
            num_per_chal[challenge] = num_per_chal[challenge] + (len(self.players)-sum(num_per_chal.values()))

        # assign people to challenges based on votes
        assignments = {"NAV": [], "ENG": [], "SCI": [], "DEF": []}
        to_assign = copy.deepcopy(self.player_ids)

        # for each challenge
        for challenge, num_participants in num_per_chal.items():
            # assign the number of people who belong in that room
            for i in range(min(len(to_assign),num_participants)):
                # figure out who received votes to participate in this challenge
                votes_for_this_chal = []
                [votes_for_this_chal.extend(v[challenge]) for v in challenge_votes]
                # only include those who have not been assigned
                votes_for_this_chal = [v for v in votes_for_this_chal if v in to_assign]
                if len(votes_for_this_chal) > 0:
                    # figure out who to assign
                    player_assigned = mode(votes_for_this_chal)
                    assignments[challenge].append(player_assigned)
                    to_assign.remove(player_assigned)

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
                actions, sabotaged, flips = challenge.check_in_all_players(participants)
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


if __name__ == '__main__':
    game = Game(6, 1)
