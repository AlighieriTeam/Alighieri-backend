from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)
@views.route('/')
@views.route('/home')
def home_page():

    return render_template("home.html")

@views.route('/room')
def room():
    from .game import games, Game

    return render_template("room.html", games=games)

@views.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method =='POST':
        from . import active_games
        pin = request.form.get('pin')
        game_list = list(filter(lambda x: x.pin == pin, active_games))
        # if game does not exist
        if len(game_list) == 0:
            # TODO: throw error with flash
            render_template("choose.html")

        # TODO: redirect to game page
        pass
    return render_template("choose.html")

@views.route('/game')
def game():
    from .game import players
    return render_template("game.html", players=players)    # pass player list of object to subsite