from flask import render_template, request


def game_of_king():
    if request.method == 'POST':
        number_of_round = request.form.getlist('number_of_round')[0]
        result=[]
        input_human_player_result = request.form.getlist('input_human_player_result')
        input_resultat_of_players = request.form.getlist('input_resultat_of_players')
        human_player_point = 0
        print(f"""number_of_rounds: {number_of_round}""")
        print(f"""input_resultat_of_players: {input_resultat_of_players}""")
        print(f"""input_human_player_result: {input_human_player_result}""")

        if input_human_player_result == 'lose':
            human_player_point -= 1
        elif input_human_player_result == 'win':
            human_player_point += 1
        return render_template('bonus/game_of_king.html', result=result, number_of_round=number_of_round, human_player_point=human_player_point)
    return render_template('bonus/game_of_king.html', number_of_round = 1, human_player_point=0)