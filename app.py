from flask import Flask, redirect, render_template, request, send_file
from uuid import uuid4
from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms
from html import escape
from json import loads

app = Flask(__name__)
app.config["SECRET_KEY"] = str(uuid4())
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")




@app.route("/")
def create_room():
    room_uuid = str(uuid4())
    return redirect(f"/{room_uuid}")


@app.route("/client_download")
def client_download():
    return send_file("./dist/game-negotiator-setup.exe", as_attachment=True)


@app.route("/<room_id>")
def load_room(room_id):
    room_id = escape(room_id)
    return render_template("room.html", room_id=room_id)


@app.route("/report_game_data", methods=["POST"])
def report_game_data():
    print(request.json)
    emit("reported_game_data", request.json, to=request.json["room_id"], namespace="/")
    return "", 200


@socketio.on("join_room")
def bind_to_room(room_data):
    room_id = room_data["room_id"]
    name = escape(room_data["name"])
    if not (len(name) > 22):
        join_room(room_id)
        emit("user_connected", {"name": name}, to=room_id)
        print(f"USER CONNECTED: {name}")


@socketio.on("user_announce")
def user_announce(data):
    data["name"] = escape(data["name"])
    emit("user_announce", data, to=data["room_id"])
    print(f"USERANNOUNCE: {data}")


@socketio.on("request_games_list")
def relay_request_games_list(data):
    room_id = data["room_id"]
    print(data)
    emit("request_games_list", data, to=room_id)


@socketio.on("games_list")
def relay_games_list(data):
    room_id = data["room_id"]
    print(data)
    emit("games_list", data, to=room_id)


socketio.run(app, host="0.0.0.0", port=80, debug=True)