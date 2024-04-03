import Player


class Challenge:
    def __init__(self, name):
        # name of challenge
        self.name = name
        # room score for this round
        self.score = 0
        # room sabotage state for this round
        self.sabotaged = False
        # dictionary of participant ID and their flip bool
        self.flips = {}

    ''' Process whether each player flips or stays '''
    def check_in_all_players(self, participants):
        action = {}
        sabotaged = False
        flips = 0
        for player in participants:
            action[player] = player.check_in_for_challenge(participants)
            # if they choose to flip, record
            if action[player]:
                if player.saboteur:
                    sabotaged = True
                else:
                    flips = flips + 1
        return action, sabotaged, flips

    ''' Process how each player does in the challenge. If more than half of the players succeed, the team succeeds. '''
    def complete_challenge_for_all_players(self, players):
        completed_successfully = []
        for participant in players:
            completed_successfully.append(participant.complete_challenge(self.name)[0])
        # number of successful completions divided by possible completions
        if len(completed_successfully) != 0:
            percent_success = sum(completed_successfully)/len(completed_successfully)
        else:
            percent_success = 1
        if percent_success >= 0.5:
            return True
        else:
            return False


