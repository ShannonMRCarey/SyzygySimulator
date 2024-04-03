import Player


class Challenge:
    def __init__(self):
        # list of player objects participating in this challenge
        self.players = []
        # room score for this round
        self.score = 0
        # room sabotage state for this round
        self.sabotaged = False
        # dictionary of participant ID and their flip bool
        self.flips = {}

    ''' sets up and runs one round of this challenge class '''
    def run_challenge(self, players, score):
        self.players = players
        self.score = score
        self.sabotaged = False
        self.flips = {}
        self.check_in_all_players()
        completed_successfully = self.complete_challenge_for_all_players()
        if completed_successfully:
            # num players * flip sign if sabotaged + flip however many individual votes again
            score = len(self.players) * (-1 * self.sabotaged) + (-1 * (not self.sabotaged) * sum(self.flips.values()))
        return score

    ''' Process whether each player flips or stays '''
    def check_in_all_players(self):
        for participant in self.players:
            if participant.saboteur:
                self.sabotaged = participant.check_in_for_challenge()
            else:
                flip = participant.check_in_for_challenge()
                self.flips[participant.id] = flip

    ''' Process how each player does in the challenge. If more than half of the players succeed, the team succeeds. '''
    def complete_challenge_for_all_players(self):
        completed_successfully = []
        for participant in self.players:
            completed_successfully.append(participant.complete_challenge())
        # number of successful completions divided by possible completions
        percent_success = sum(completed_successfully)/len(completed_successfully)
        if percent_success >= 0.5:
            return True
        else:
            return False


