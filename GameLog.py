from pprint import pprint

class GameLog:
    def __init__(self, num_players, num_saboteurs):
        self.num_players = num_players
        self.num_saboteurs = num_saboteurs
        open("GameLog.txt", 'w').close()
        self.log = open("GameLog.txt", "a")

    def log_players(self, players):
        self.log.write("...INTRODUCING...\n")
        for p in players:
            self.log.write(f'Player {p.id}')
            if p.saboteur: self.log.write(": THE SABOTEUR")
            self.log.write(f'\n\tNAV Skill: {p.nav_skill}\n')
            self.log.write(f'\tENG Skill: {p.eng_skill}\n')
            self.log.write(f'\tSCI Skill: {p.sci_skill}\n')
            self.log.write(f'\tDEF Skill: {p.def_skill}\n')

    def log_round(self, round, score):
        self.log.write(f'\n---ROUND {round}---\n')
        self.log.write(f'SCORE: {score}\n')

    def log_mission(self, mission, selected_mission):
        self.log.write(f'Mission Options: {mission}\n')
        self.log.write(f'Selected Mission: {selected_mission}\n')

    def log_mission_loss(self, selected_mission, points):
        self.log.write(f'Mission will lose the team {points} from {selected_mission}\n')

    def log_challenges(self, name, participants):
        if len(participants) > 0:
            self.log.write(f'In {name}\n')
            self.log.write(f'\tPlayers {participants}\n')

    def log_actions(self, actions, challenge):
        for player, flip in actions.items():
            if not player.saboteur:
                if flip:
                    self.log.write(f'\t{challenge}: Player {player.id} chooses to FLIP\n')
                else:
                    self.log.write(f'\t{challenge}: Player {player.id} chooses not to FLIP\n')
            else:
                if flip:
                    self.log.write(f'\t{challenge}: SABOTEUR chooses to SABOTAGE\n')
                else:
                    self.log.write(f'\t{challenge}: SABOTEUR chooses NOT to SABOTAGE\n')

    def log_challenge_outcomes(self, name, succeeded):
        if succeeded:
            self.log.write(f'\tThe {name} team was SUCCESSFUL!\n')
        else:
            self.log.write(f'\tThe {name} team was NOT SUCCESSFUL.\n')

    def score_log(self, name, this_score, new_score):
        self.log.write(f'\tTeam scored {this_score} points for room.\n')