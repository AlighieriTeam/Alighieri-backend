from flask import Flask
from .room import Room

active_games: list[Room] = []
def create_app():
    app = Flask(__name__)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app