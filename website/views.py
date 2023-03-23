from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)
@views.route('/')
@views.route('/home')
def home_page():

    return render_template("home.html")

@views.route('/room', methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        from .game import players
        import random
        pin = str(random.randint(1000, 9999))
        return render_template("room.html", players=players, game_pin=pin)

    # if tried to enter /room directly - redirect to choose
    return redirect(url_for('.choose'))


@views.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        from .game import players

        pin = request.form.get('pin')
        return render_template("join.html", players=players, game_pin=pin)

    # if tried to enter /join directly - redirect to choose
    return redirect(url_for('.choose'))

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