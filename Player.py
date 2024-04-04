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
    def vote_for_assignments(self, selected_mission, score):
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

        # starting with the lowest scoring room, add people
        while num_to_assign > 0:
            # runs assignment function
            challenge, num_assigned = self.assigning(considered_score, num_to_assign)
            assignments[challenge] = sorted_trust[0:num_assigned]
            # updates list of remaining challenges, scores, and people left to consider
            considered_score.pop(challenge)
            for i in assignments[challenge]:
                sorted_trust.remove(i)
            num_to_assign = num_to_assign-num_assigned
        return assignments

    def assigning(self, considered_score, num_to_assign):
        # figure out how many people you want in the room
        lowest_score = min(considered_score.values())
        challenge = [key for key, val in considered_score.items() if val == lowest_score][0]
        #TODO: design something more robust!
        assigned = min(2, math.ceil(num_to_assign / 2))
        return challenge, assigned

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
    not global score) and assignments {player_id: challenge, player_id: challenge ... player_id: challenge'''
    def update_trust(self, score, assignments):
        for player_id, challenge in assignments.items():
            # we continue to trust ourselves
            if player_id == self.id:
                trust_update = 0
            else:
                if score[challenge] == 0:
                    trust_update = 0
                else:
                    trust_update = self.relationships[player_id]/score[challenge]
            self.relationships[player_id] = self.relationships[player_id] + trust_update
        return self.relationships.values()
