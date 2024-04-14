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
        self.trust_threshold = self.trust/2
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

        # we predict out what the next score will be but subtracting the average mission penalty for selected mission
        considered_score = copy.deepcopy(score)
        considered_score[selected_mission] = considered_score[selected_mission]-2

        # Get the scores from lowest to highest
        sorted_score = sorted(considered_score.items(), key=lambda item: item[1])
        sorted_score = [challenge for (challenge, score) in sorted_score]

        # Normalize trust scores
        total_trust = sum(self.relationships.values())
        for person, trust in self.relationships.items():
            self.relationships[person] = round(trust/total_trust,2)

        # Get the IDs of everyone you trust in order (if saboteur, prioritize other sketchy-looking people)
        sorted_trust = sorted(self.relationships.items(), key=lambda item: item[1])
        sorted_trust = [id for (id, trust) in sorted_trust]
        # Good guys want the person they trust most first in the list
        if not self.saboteur:
            sorted_trust.reverse()

        # figure out how many people should be in a room, in order of room priority/importance (lowest score)
        for chal in sorted_score:
            score_deficit = starting_score - score[chal]
            # find the number of participants who will give us the highest expected value
            num_participants_for_best_outcome = 0
            best_score = 0
            for num_participants in range(2, len(self.all_ids)+1):
                # 1 and n-1 are not valid numbers because you can't have one person alone in a room
                if not num_participants == len(self.all_ids)-1:
                    # TODO: add risk multiplier so we don't always pick 2
                    max_score = num_participants
                    # the chances that all of these people are good at once
                    trust_slice = [self.relationships[p] for p in sorted_trust[0:num_participants]]
                    trust_product = np.prod(trust_slice)
                    expected_score = max_score * trust_product
                    if expected_score > best_score:
                        num_participants_for_best_outcome = num_participants
                        best_score = expected_score
            # assign the first n trusted people to the challenge, and remove those people from consideration
            assignments[chal] = sorted_trust[:num_participants_for_best_outcome]
            sorted_trust = sorted_trust[num_participants_for_best_outcome:]
        return assignments

    def check_in_for_challenge(self, challenge_participants):
        # true for a flip or sabotage, false for no flip or sabotage
        flip = False
        # if we knew nothing about anyone but ourselves, what's the chance that one of these people is the saboteur?
        random_chance = (len(challenge_participants) - 1) / (len(self.all_ids) - 1)
        if self.saboteur:
            # if we think the random chance is high, it means there's a good chance we get away with this
            choice = random.choices([True, False], weights=[random_chance, 1-random_chance], k=1)
            return choice
        else:
            if 1-random_chance < self.trust_threshold:
                return True
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
            for player_id in player_ids:
                players_considered = len(player_ids)
                # if we were in the room, don't count ourselves towards our suspicions
                if self.id in player_ids:
                    players_considered -= 1
                # we continue to trust ourselves
                if player_id == self.id:
                    trust_update = 0
                else:
                    # this should never happen but jic
                    if players_considered == 0:
                        trust_update = 0
                        print("WARNING: you shouldn't be able to get here!")
                    else:
                        curr_trust = self.relationships[player_id]
                        if score[challenge] > 0:
                            # if n people contributed to this room score trust moves 1/n of the remaining dist up
                            trust_update = (1-curr_trust)/players_considered
                        else:
                            # if n people contributed to this room score trust moves 1/n of the remaining dist down
                            trust_update = -curr_trust/players_considered
                self.relationships[player_id] = self.relationships[player_id] + trust_update
        return self.relationships.values()
