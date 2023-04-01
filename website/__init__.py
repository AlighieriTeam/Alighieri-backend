from flask import Flask
from .room import Room

active_games: list[Room] = []

def find_game(pin: str):
    for game in active_games:
        if game.pin == pin:
            return game
    return None

def create_app():
    app = Flask(__name__)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app