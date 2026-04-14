import socketio
import time

sio = socketio.Client()
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImthaXplbiIsImV4cCI6MTc3NjIyMzg1OH0.JaueEbRXVuShwFVSTowi0vZtI22FO1x8wwn-vVfb2KY"

@sio.on("user_joined")
def on_join(data):
    print(f">> {data['username']} joined the room")

@sio.on("new_message")
def on_message(data):
    print(f"[{data['username']}]: {data['content']}")

@sio.on("user_left")
def on_leave(data):
    print(f">> {data['username']} left the room")

sio.connect("http://127.0.0.1:8000")
print("Connected!")

sio.emit("join", {"token": TOKEN, "room_id": 1})
time.sleep(1)

sio.emit("send_message", {"token": TOKEN, "room_id": 1, "content": "Hello everyone!"})
time.sleep(1)

sio.emit("send_message", {"token": TOKEN, "room_id": 1, "content": "This is real-time!"})
time.sleep(1)

sio.emit("leave", {"token": TOKEN, "room_id": 1})
time.sleep(1)

sio.disconnect()
print("Done!")
