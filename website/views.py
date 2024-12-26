from flask import Blueprint,render_template,request,flash,redirect,url_for,session,after_this_request
from . import db
from .Models import Game_players
from sqlalchemy import and_
import random
from string import ascii_uppercase
from threading import Timer
import socket
#from main import IPAddr

views = Blueprint('views',__name__)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

rooms = {}

def generate_unique(Length):
    while True:
        code = ""
        for _ in range(Length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

@views.route("/",methods = ["POST","GET"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join =  request.form.get("join",False)
        create = request.form.get("create",False)

        result = db.session.query(
            db.exists().where(
                    getattr(Game_players, 'user_name_code') == (name.lower() + " " + code)
                )
            ).scalar()

        if not name:
            flash('please enter name',category = 'error')

        elif join != False and not code:
            flash('please enter a room code',category = 'error')

        elif join != False and result:
            flash('name already exists',category = 'error')

        else:
            room = code
            if create != False:
                room = generate_unique(4)
                user_name_code = name.lower() + " " + room
                new_user = Game_players(user_name_code = user_name_code,active_state = 'waiting',points = 0,turns = 0) 
                db.session.add(new_user)
                db.session.commit()
                rooms[room] = {"members":0, "messages": []}
                session["room"] = room
                session["name"] = name.lower()

                return redirect(url_for("views.room"))

            elif code not in rooms:
                flash('room does not exists',category = 'error')

            else:
                user_name_code = name.lower() + " " + room
                new_user = Game_players(user_name_code = user_name_code,active_state = 'waiting',points = 0,turns = 0) 
                db.session.add(new_user)
                db.session.commit()

                session["room"] = room
                session["name"] = name.lower()

                return redirect(url_for("views.room"))

    return render_template("home.html")

@views.route("/room",methods = ["POST","GET"])
def room():
    name = session.get("name")
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("views.home"))
    
    users = Game_players.query.all()
    user_names = [user.user_name_code for user in users]

    print(user_names)
    print(name + " " +room)
    player = Game_players.query.get(name + " " +room)
    user_active_state = player.active_state
    

    return render_template("room.html",code=room,messages = rooms[room]["messages"],name=name,ip = IPAddr)
