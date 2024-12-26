from website import create_app, db
from website.views import rooms
from flask import session,flash,request
from flask_socketio import join_room, leave_room, send, SocketIO, emit
from website.Models import Game_players
import socket
import random as r
import pickle

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = create_app()
socketio = SocketIO(app,cors_allowed_orgins = "*")

socketids = {}
game_words = {}
turn_numbers = {}
player_points = {}
correct_number = {}
game_started = []
round_starting_checker = {}

def round(name_code,room):
    turn_numbers[room] += 1
    turn_number = turn_numbers[room]

    print("turn: ",turn_number)
    print("namelen: ",len(name_code))

    if turn_number >= len(name_code):
        print("game over")
        top_points = max(player_points[room].values())

        for i in player_points[room].keys():
            if player_points[room][i] == top_points:
                winner = i
                break

        emit("game_over",{"name":winner,"points":top_points},room=room)

    else:
        emit("btn_state",{"state": "active"},room=room)
        word = []
        with open("wordList.dat","rb") as file:
            l = pickle.load(file)

            for i in range(3):
                while True:
                    w = l[r.randint(0,len(l)-1)]
                    if w not in game_words[room] and w not in word:
                        game_words[room].append(w)
                        word.append(w)
                        break
        
        name = name_code[turn_number].split()[0]
        emit("flash_message", {"message": f"{name} choosing a word", "category": "error"}, room=room)
        emit("btn_state",{"state":"drawing","word1":f"{word[0]}","word2":f"{word[1]}","word3":f"{word[2]}","id":f"{socketids[name_code[turn_number]]}","room":f"{room}","name":f"{name}"},to = socketids[name_code[turn_number]], room=room)


def start_game(room):
    players = Game_players.query.filter(Game_players.user_name_code.like(f'%{room}%'))
    game_words[room] = []
    turn_numbers[room] = -1
    player_points[room] = {}
    correct_number[room] = 0
    game_started.append(room)
    round_starting_checker[room] = 0

    player_names = []
    for i in players:
        player_names.append(i.user_name_code)
        name_code = i.user_name_code
        name = name_code.split(" ")[0]
        print("room : ",room," name: ",name)
        player_points[room][name] = 0

    round(player_names,room)
    

def check_no_players(room, membersCount):
    name = session.get("name")

    print(f"check: {name} : {room}")
    user = name + " " + room

    if membersCount < 2:
        emit("btn_state",{"state": "waiting"},room=room)
        print("players too few")
        emit("flash_message", {"message": f"{membersCount}/2 players waiting for more", "category": "error"}, room=room)

    else:
        emit("flash_message", {"message": "All players have joined, let the game begin", "category": "success"}, room=room)
        players = Game_players.query.filter(Game_players.user_name_code.like(f'%{room}%'))
        

        for i in players:
            i.active_state = "active"
        
        db.session.commit()

        for i in players:
            print(f"{i.user_name_code} : {i.active_state}")

        emit("btn_state",{"state": "active"},room=room)
        if room not in game_started:
            start_game(room)

@socketio.on('start_next_round')
def handle_start_next_round(data):
    room = data['room']
    name = data['name']

    print(f"{round_starting_checker}")

    if round_starting_checker[room] == 0:
        players = Game_players.query.filter(Game_players.user_name_code.like(f'%{room}%'))
        round_starting_checker[room] = 1

        player_names = []
        for i in players:
            player_names.append(i.user_name_code)
            
        round(player_names,room)
        print("hello")


@socketio.on('round_end')
def handle_round_end(data):
    room = data['room']
    word = data['word']
    name = data['name']

    round_starting_checker[room] = 0

    names = list(player_points[room].keys())
    points = list(player_points[room].values())

    emit("btn_state",{"state": "waiting"},room=room)
    emit("canvas_clear",room=room)
    emit("round_end_display",{"word":word,"room":room,"names":names,"points":points,"name":name},room=room)

@socketio.on('canvas_data')
def handle_canvas_data(data):
    print("canvas_updating")
    canvas_data = data["data"]
    room  = session.get("room")

    emit("canvas_update",{"data": canvas_data}, room=room)



@socketio.on('wordDisplay')
def handle_word_display(data):
    word =  data['word']
    id = data['id']
    room = data['room']
    name = data['name']

    print(f'Word: {word}, ID: {id}')
    emit("flash_message", {"message": f"word chosen", "category": "error"}, room=room)
    emit("word-display",{"word":word,"id":id},room=room)
    emit("start_timer",{"starttime" : 2,"room" : room,'name' : name},room=room)

@socketio.on('correct_answer')
def handle_correct_answer(data):
    name = data['name']
    room  = session.get("room")
    word = data['word']
    time = data['time']

    correct_number[room] +=1

    minutes_sec = time.split(":")
    minutes = int(minutes_sec[0])
    seconds = int(minutes_sec[1])

    print("number: ",correct_number[room])

    total_time_value = minutes*100 + seconds
    print("room : ",room," name: ",name)
    player_points[room][name] += total_time_value

    user = name + " " + room

    emit("btn_state",{"state": "waiting"},to = socketids[user],room=room)
    emit("correct_answer_display",{"word": word},to = socketids[user],room=room)
    emit("flash_message", {"message": "You guessed the correct answer", "category": "success"},to = socketids[user], room=room)

    if correct_number[room] == 1:
        print("all players got it correct")
        correct_number[room] = 0
        emit("start_timer",{"starttime" : 0,"room" : room,'name' : name},room=room)

 

@socketio.on("connect")
def connect(auth):
    room  = session.get("room")
    name = session.get("name")

    if not room or not name:
        return
    
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to = room)
    rooms[room]["members"] += 1

    user_code = name + " " + room

    socketids[user_code] = request.sid

    check_no_players(room,rooms[room]["members"])
    
    print(f"{name} joined room {room}")


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    name = session.get("name")
    user_code = name + " " + room
    content = {
        "name": name,
        "message": data["data"],
        "socketid": socketids[user_code]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)

    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

        user_code = name + " " + room
        del socketids[user_code]
        with app.app_context():
            db.session.delete(Game_players.query.get(user_code))
            db.session.commit()
            print(f"deleted {user_code}")


    send({"name": name, "message": "has left the room"}, to = room)
    print(f"{name} left room {room}")

    


if __name__ == "__main__":
    socketio.run(app,host=f"{IPAddr}",debug = True)