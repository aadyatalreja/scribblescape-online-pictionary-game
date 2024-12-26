from . import db
from sqlalchemy.sql import func

class Game_players(db.Model):
    user_name_code = db.Column(db.String(150),primary_key = True)
    active_state = db.Column(db.String(150))
    points = db.Column(db.Integer)
    turns = db.Column(db.Integer)
