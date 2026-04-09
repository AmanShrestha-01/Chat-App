from flask_socketio import SocketIO, emit, join_room, leave_room
from models import db, Message
import datetime
import jwt

socketio = SocketIO()
SECRET_KEY = "your-secret-key-change-this-later"

online_users = {}

@socketio.on("connect")
def handle_connect():
    print("Someone connected")

@socketio.on("join")
def handle_join(data):
    token = data.get("token")
    room_id = data.get("room_id")
    if not token or not room_id:
        return
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return
    room = str(room_id)
    join_room(room)
    online_users[user["username"]] = room
    emit("user_joined", {"username": user["username"]}, room=room)

@socketio.on("send_message")
def handle_message(data):
    token = data.get("token")
    room_id = data.get("room_id")
    content = data.get("content")
    if not token or not room_id or not content:
        return
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return
    message = Message(
        room_id=room_id,
        user_id=user["user_id"],
        username=user["username"],
        content=content,
        created_at=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(message)
    db.session.commit()
    room = str(room_id)
    emit("new_message", {
        "username": user["username"],
        "content": content,
        "created_at": message.created_at
    }, room=room)

@socketio.on("leave")
def handle_leave(data):
    token = data.get("token")
    room_id = data.get("room_id")
    if not token or not room_id:
        return
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return
    room = str(room_id)
    leave_room(room)
    if user["username"] in online_users:
        del online_users[user["username"]]
    emit("user_left", {"username": user["username"]}, room=room)

@socketio.on("disconnect")
def handle_disconnect():
    print("Someone disconnected")
