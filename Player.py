import random
import numpy as np
import math
import copy

class Player:
    def __init__(self, player_id, saboteur, all_ids):
        self.id = player_id
        self.all_ids = all_ids
        self.saboteur = saboteur
        # random numbers between 0 and 1 to represent this player's skills and personality
        self.trust = round(random.random(), 2)
        self.trust_threshold = 0.25
        self.intelligence = round(random.random(), 2)
        self.nav_skill = round(random.random(), 2)
        self.eng_skill = round(random.random(), 2)
        self.sci_skill = round(random.random(), 2)
        self.def_skill = round(random.random(), 2)
        self.skill_map = {"NAV": self.nav_skill,
                          "ENG": self.eng_skill,
                          "SCI": self.sci_skill,
                          "DEF": self.def_skill}
        # represent trust of other players
        # assumes we start by trusting everyone equally, except ourselves
        starting_trust_array = np.full(shape=len(self.all_ids), fill_value=self.trust)
        self.relationships = dict(zip(self.all_ids, starting_trust_array))
        # we always trust ourselves (right?)
        self.relationships[self.id] = 1

    '''player returns the mission they vote for. Takes in mission [string, string] and score
    {NAV:int score, ENG: int score, SCI: int score, DEF: int score}'''
    def vote_for_mission(self, mission, score):
        # low intel players choose the mission they have more skill in
        relevant_skills = [self.skill_map[challenge] for challenge in mission]
        skill_based_choice = random.choices(mission, weights=relevant_skills, k=1)[0]

        # high intel players choose the mission with the highest score
        relevant_scores = dict([(challenge,score[challenge]) for challenge in mission])
        score_based_choice = max(relevant_scores)

        # use intelligence as a weight for random choice between skill and score
        choice = random.choices([skill_based_choice, score_based_choice],
                                weights=[1-self.intelligence, self.intelligence],
                                k=1)
        return choice

    '''player returns the assignment dict they vote for. Takes in selected_mission string and score
        {NAV:int score, ENG: int score, SCI: int score, DEF: int score}, returns {"NAV": [id], "ENG": [id],
         "SCI": [id], "DEF": [id]} '''
    def vote_for_assignments(self, selected_mission, starting_score, score):
        assignments = {"NAV": [], "ENG": [], "SCI": [], "DEF": []}
        num_to_assign = len(self.all_ids)
        # we use a copy of the score to track the challenges to assign (which is based on score)
        considered_score = copy.deepcopy(score)
        considered_score[selected_mission] = considered_score[selected_mission]-2

        # Get the IDs of everyone you trust in order (if saboteur, prioritize other sketchy-looking people)
        sorted_trust = sorted(self.relationships.items(), key=lambda item: item[1])
        sorted_trust = [id for (id, trust) in sorted_trust]
        # Good guys want the person they trust most first in the list
        if not self.saboteur:
            sorted_trust.reverse()

        # number of people to assign to each challenge in form {"NAV": int, "ENG": int, "SCI": int, "DEF": int}
        number_to_assign_per_chal = self.determine_number_to_assign(starting_score, considered_score)

        # sort them so that we assign by order of challenge importance/low score
        ordered_number_to_assign_per_chal = {k: v for k, v in sorted(number_to_assign_per_chal.items(),
                                                                     key=lambda item: item[1],
                                                                     reverse=True)}
        print(f'ordered number to assign per challenge: {ordered_number_to_assign_per_chal}')

        # While anyone is still unassigned, keep assigning them in order of trust
        while num_to_assign > 0:
            for challenge, assigning in ordered_number_to_assign_per_chal.items():
                assignments[challenge] = sorted_trust[0:assigning]
                print(f'Assigning {sorted_trust[0:assigning]} to {challenge}')
                # updates list of remaining challenges, scores, and people left to consider
                considered_score.pop(challenge)
                for i in assignments[challenge]:
                    sorted_trust.remove(i)
                num_to_assign -= assigning
        return assignments

    def determine_number_to_assign(self, starting_score, considered_score):
        # Figure out how many people to assign to each challenge
        left_to_assign = len(self.all_ids)
        number_to_assign_per_chal = {"NAV": 0, "ENG": 0, "SCI": 0, "DEF": 0}
        # TODO: come up with different logics, eg. refuse to put anyone with <0.25 trust in a key room
        # Aim to get every score back up to its original
        score_deficit = {"NAV": 0, "ENG": 0, "SCI": 0, "DEF": 0}
        for challenge in score_deficit.keys():
            score_deficit[challenge] = starting_score - considered_score[challenge]
        # takes the number of players left to assign and the highest deficit challenge and adds a player to that chal
        def num_per_chal_assigner(left_to_assign, challenge):
            number_to_assign_per_chal[challenge] += 1
            left_to_assign -= 1
            score_deficit[challenge] -= 1
            return left_to_assign, score_deficit

        while left_to_assign > 0:
            print(f'remaining to assign: {left_to_assign}')
            highest_deficit = max(score_deficit.values())
            print(f'highest deficit: {highest_deficit} (of {score_deficit})')
            challenge = [key for key, val in score_deficit.items() if val == highest_deficit][0]
            left_to_assign, score_deficit = num_per_chal_assigner(left_to_assign, challenge)

        # if any challenge has exactly one participant, move that participant to the challenge with the lowest score
        for challenge, assignees in number_to_assign_per_chal.items():
            if assignees == 1:
                number_to_assign_per_chal[challenge] = 0
                low_score = min(considered_score.values())
                lowest_challenge = [key for key in considered_score if considered_score[key] == low_score][0]
                print(f'reassigning 1 from {challenge} to {lowest_challenge}')
                number_to_assign_per_chal[lowest_challenge] += 1

        return number_to_assign_per_chal

    def check_in_for_challenge(self, challenge_participants):
        # true for a flip or sabotage, false for no flip or sabotage
        # where challenge_participants is a list of Player IDs
        flip = False
        if self.saboteur:
            # TODO: more complicated logic here
            return True
        else:
            for player in challenge_participants:
                if self.relationships[player.id] < self.trust_threshold:
                    return True
                else:
                    return False

    '''Simulates player actually preforming the challenge they were assigned to. Takes in challenge string,
    returns True if successful.'''
    def complete_challenge(self, challenge):
        skill = self.skill_map[challenge]
        return random.choices([True, False], weights=[skill, 1-skill], k=1)

    '''Simulates the player re-evaluating their trust of others based on how each room did this round. Takes in
    score {NAV:int score, ENG: int score, SCI: int score, DEF: int score} (where score is what happened this round,
    not global score) and assignments {NAV: [ids in nav], ENG: [ids in eng] ... DEF: [ids in def]'''
    def update_trust(self, score, assignments):
        for challenge, player_ids in assignments.items():
            # we continue to trust ourselves
            for player_id in player_ids:
                if player_id == self.id:
                    trust_update = 0
                else:
                    if score[challenge] == 0:
                        trust_update = 0
                    else:
                        trust_update = self.relationships[player_id]/score[challenge]
            self.relationships[player_id] = self.relationships[player_id] + trust_update
        return self.relationships.values()
