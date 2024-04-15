import Game

# set of player numbers to test
players = [6, 8, 10, 12]

# number of games to run
n = 500

# difficulty (1=Easy, 2=Med, 3=Hard)
difficulty = 2

# number of saboteurs
saboteurs = [1, 2]

for s in saboteurs:
    for p in players:
        # record the number of wins and average score
        wins = 0
        average_scores = []
        # run n games with this many players
        for g in range(n):
            game = Game.Game(p, s, difficulty, False)
            score, win = game.analytics
            if win:
                wins += 1
            average_score = sum(score.values())/4
            average_scores.append(average_score)

        print(f'Players: {p}')
        print(f'Saboteurs: {s}')
        print(f'win percentage: {wins/n:.0%}')
        print(f'average score: {sum(average_scores)/n}')
