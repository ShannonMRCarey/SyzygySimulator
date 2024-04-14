import matplotlib.pyplot as plt
import webbrowser
import pandas as pd


class TextGameLog:
    def __init__(self, num_players, num_saboteurs):
        self.log_images = False
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
            self.log.write(f'\tThe {name} team was NOT SUCCESSFUL\n')

    def score_log(self, name, this_score, new_score):
        self.log.write(f'\tTeam scored {this_score} points for room\n')

    '''the rows in relationships_df represent how each player feels about all the others'''
    def trust_update_log(self, relationships_df):
        self.log.write(f'Player relationships updated\n')
        if self.log_images:
            plt.imshow(relationships_df, cmap="RdYlBu")
            plt.colorbar()
            plt.xticks(range(len(relationships_df)), relationships_df.columns)
            plt.yticks(range(len(relationships_df)), relationships_df.index)
            plt.show()
        # else:
        #     print(relationships_df)

    def conclusion_log(self, score):
        self.log.write(f'Final Score: {score}\n')
        if min(list(score.values())) < 0:
            self.log.write("The SABOTEUR has won! The team did not successfully stop them.\n")
        else:
            self.log.write("The TEAM Wins! The Saboteur was unsuccessful.\n")

class HTMLGameLog:
    def __init__(self, num_players, num_saboteurs):
        self.log_images = False
        self.num_players = num_players
        self.num_saboteurs = num_saboteurs

        self.active_challenges = []
        self.challenge_flips = []
        self.challenge_outcomes = []
        self.challenge_score = []

        self.file = "GameLog.html"
        open(self.file, 'w').close()
        self.log = open(self.file, "a")

        self.log.write('<html>')
        self.log.write('<head>')
        self.log.write('<link href = "styles/style.css" rel = "stylesheet" / >')
        self.log.write('<title> Syzygy </title>')
        self.log.write('</head>')

    def log_players(self, players):
        self.log.write('<body>')
        self.log.write('<div class="intro">')
        self.log.write('<br>')
        self.log.write('<h1> INTRODUCING </h1>')
        self.log.write('<table style="width:50%" class="center">')
        self.log.write('<tr>')
        for p in players:
            self.log.write(f'<th>Player {p.id}</th>')
        self.log.write('</tr>')
        self.log.write('<tr>')
        for p in players:
            self.log.write('<td>')
            self.log.write('<br>')
            self.log.write(f'Trust: {p.trust:.0%}<br>')
            self.log.write(f'Intelligence: {p.intelligence:.0%}<br>')
            self.log.write('<br>')
            self.log.write(f'NAV: {p.nav_skill:.0%}<br>')
            self.log.write(f'ENG: {p.eng_skill:.0%}<br>')
            self.log.write(f'SCI: {p.sci_skill:.0%}<br>')
            self.log.write(f'DEF: {p.def_skill:.0%}<br>')
            if p.saboteur:
                self.log.write(f'<span style="background-color:#ad3624">')
                self.log.write('<br>THE SABOTEUR<br>')
                self.log.write('</span>')
            self.log.write('</td>')
        self.log.write('</tr>')
        self.log.write('</table>')
        self.log.write('<br><br>')
        self.log.write('</div>')

    def log_round(self, round, score):
        self.active_challenges = []
        self.challenge_flips = []
        self.challenge_outcomes = []
        self.challenge_score = []

        self.log.write('<div class="round">')
        self.log.write('<br><br>')
        self.log.write('<table style="width:60%" class="center">')
        self.log.write('<tr>')
        self.log.write(f'<th style="width:15%">ROUND<br>{round}</th>')

        self.log.write('<td style="width:10%">')
        for chal, num in score.items():
            self.log.write(f'{chal} {num}<br>')
        self.log.write('</td>')

    def log_mission(self, mission, selected_mission):
        self.log.write('<td style="width:10%">')
        for m in mission:
            if m == selected_mission:
                self.log.write(f'<b>{m}</b><br>')
            else:
                self.log.write(f'{m}<br>')
        self.log.write('</td>')

    def log_mission_loss(self, selected_mission, points):
        self.log.write(f'<td style="width:10%"> {selected_mission} -{points}  </td>')

    def log_challenges(self, challenge, participants):
        if len(participants) > 0:
            self.active_challenges.append(challenge)

    def log_actions(self, actions, challenge):
        html_friendly_actions = ""
        for player, flip in actions.items():
            if not player.saboteur:
                if flip:
                    html_friendly_actions +='Player ' + str(player.id) + ': FLIP<br>'
                else:
                    html_friendly_actions +='Player ' + str(player.id) + ': no flip<br>'
            else:
                if flip:
                    html_friendly_actions +='Player ' + str(player.id) + ': SABOTAGE<br>'
                else:
                    html_friendly_actions +='Player ' + str(player.id) + ': no sabotage<br>'
        self.challenge_flips.append(html_friendly_actions)

    def log_challenge_outcomes(self, name, succeeded):
        if succeeded:
            self.challenge_outcomes.append(f'SUCCESSFUL')
        else:
            self.challenge_outcomes.append(f'UNSUCCESSFUL')

    def score_log(self, name, this_score, new_score):
        if this_score < 0:
            self.challenge_score.append(f'{name}: {this_score}')
        else:
            self.challenge_score.append(f'{name}: +{this_score}')

    '''the rows in relationships_df represent how each player feels about all the others'''
    def trust_update_log(self, relationships_df):
        # First print challenge outcome
        self.log.write('<td>')
        challenge_df = pd.DataFrame(list(zip(self.active_challenges,
                                   self.challenge_flips,
                                   self.challenge_outcomes,
                                   self.challenge_score)),
                          columns=['challenge', 'choices', 'outcomes', 'scores'])
        challenge_df.set_index('challenge', inplace=True)
        self.log.write(challenge_df.to_html(classes='round',
                                            header=False,
                                            index_names=False,
                                            escape=False,
                                            border=0,
                                            justify='center'))
        self.log.write('</td>')

        # Then print updated trust
        trust_df = relationships_df.style.background_gradient(axis=0, vmin=0, vmax=1, cmap="RdYlGn").format(precision=2)
        self.log.write('<td style="width:15%">')
        self.log.write(trust_df.to_html(border=0))
        self.log.write('</td>')
        self.log.write('</table>')

    def conclusion_log(self, score):
        self.log.write(f'<h2>Final Score: {score}</h2>')
        if min(list(score.values())) < 0:
            self.log.write('<h2>The <span style="background-color:#ad3624">SABOTEUR</span> has won!</h2>')
        else:
            self.log.write("<h2>The TEAM Wins! The Saboteur was unsuccessful.</h2>")
        self.log.write('<br><br>')
        self.log.write('</div>')
        self.log.write('</body')
        self.log.write('</html>')
        webbrowser.open(self.file)
