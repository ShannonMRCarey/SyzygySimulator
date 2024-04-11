import matplotlib.pyplot as plt
import webbrowser
import base64
from io import BytesIO

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
        self.log.write('<h1> INTRODUCING </h1>')
        self.log.write('<table style="width:50%" class="center">')
        self.log.write('<tr>')
        for p in players:
            self.log.write(f'<th>Player {p.id}</th>')
        self.log.write('</tr>')
        self.log.write('<tr>')
        for p in players:
            self.log.write('<td>')
            if p.saboteur: self.log.write("THE SABOTEUR <br>")
            self.log.write(f'NAV Skill: {p.nav_skill}<br>')
            self.log.write(f'ENG Skill: {p.eng_skill}<br>')
            self.log.write(f'SCI Skill: {p.sci_skill}<br>')
            self.log.write(f'DEF Skill: {p.def_skill}<br>')
            self.log.write('</td>')
        self.log.write('</tr>')
        self.log.write('</table>')

    def log_round(self, round, score):
        self.log.write('<br><br>')
        self.log.write('<table style="width:100%">')
        self.log.write('<tr>')
        self.log.write(f'<th style="width:15%">ROUND {round}</th>')

        self.log.write(f'<td style="width:15%">{score}</td>')

    def log_mission(self, mission, selected_mission):
        for m in mission:
            if m == selected_mission:
                self.log.write(f'<td style="width:3%"><b>{m}</b></td>')
            else:
                self.log.write(f'<td style="width:3%">{m}</td>')

    def log_mission_loss(self, selected_mission, points):
        self.log.write(f' <td style="width:3%"> {selected_mission} -{points}  </td>')

    def log_challenges(self, name, participants):
        self.log.write('<td>')
        if len(participants) > 0:
            self.log.write(f'<b>{name}</b><br>')
            # self.log.write(f'<p> Players {participants}</p>')

    def log_actions(self, actions, challenge):
        for player, flip in actions.items():
            if not player.saboteur:
                if flip:
                    self.log.write(f'Player {player.id}: FLIP<br>')
                else:
                    self.log.write(f'Player {player.id}: no flip <br>')
            else:
                if flip:
                    self.log.write(f'Player {player.id}: SABOTAGE<br>')
                else:
                    self.log.write(f'Player {player.id}: no sabotage<br>')

    def log_challenge_outcomes(self, name, succeeded):
        if succeeded:
            self.log.write(f'The {name} team was SUCCESSFUL!<br>')
        else:
            self.log.write(f'The {name} team was NOT SUCCESSFUL<br>')

    def score_log(self, name, this_score, new_score):
        self.log.write(f'<p>{name}: +{this_score}</p>')
        self.log.write('</td>')

    '''the rows in relationships_df represent how each player feels about all the others'''
    def trust_update_log(self, relationships_df):
        self.log.write('<td>')
        if self.log_images:
            fig = plt.figure()
            fig.imshow(relationships_df, cmap="RdYlBu")
            fig.colorbar()
            fig.xticks(range(len(relationships_df)), relationships_df.columns)
            fig.yticks(range(len(relationships_df)), relationships_df.index)
            fig.show()
            tmpfile = BytesIO()
            fig.savefig(tmpfile, format='png')
            encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
            self.log.write('<img src=\'data:image/png;base64,{}\'>'.format(encoded))
        self.log.write('</td>')
        self.log.write('</table>')

    def conclusion_log(self, score):
        self.log.write(f'<h2>Final Score: {score}</h2>')
        if min(list(score.values())) < 0:
            self.log.write("<h2>The SABOTEUR has won! The team did not successfully stop them.</h2>")
        else:
            self.log.write("<h2>The TEAM Wins! The Saboteur was unsuccessful.</h2>")
        self.log.write('</body')
        self.log.write('</html>')
        webbrowser.open(self.file)