from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)
@views.route('/')
def home_page():

    return render_template("home.html")

@views.route('/new-game')
def new_game():
    from .game import games, Game

    return render_template("new-game.html", games=games)

@views.route('/choose-game', methods=['GET', 'POST'])
def choose_game():
    if request.method =='POST':
        from . import active_games
        pin = request.form.get('pin')
        game_list = list(filter(lambda x: x.pin == pin, active_games))
        # if game does not exist
        if len(game_list) == 0:
            # TODO: throw error with flash
            render_template("choose-game.html")

        # TODO: redirect to game page
        pass
    return render_template("choose-game.html")
