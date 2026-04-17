# Real-Time Chat API

A backend chat application with real-time messaging using WebSockets, chat rooms, and message history.

## Tech Stack

- Python, Flask
- Flask-SocketIO (WebSockets)
- SQLAlchemy, SQLite
- JWT Authentication, Bcrypt
- Swagger API Documentation

## Features

- User signup and login with hashed passwords
- JWT token-based authentication
- Create and list chat rooms
- Real-time messaging with WebSockets
- Message history stored in database
- Auto-generated API docs at /apidocs

## API Endpoints (HTTP)

| Method | URL | Description |
|--------|-----|-------------|
| POST | /signup | Create account |
| POST | /login | Log in, get token |
| POST | /rooms | Create a chat room |
| GET | /rooms | List all rooms |
| GET | /rooms/:id/messages | Get message history |

## WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| connect | Client → Server | Open connection |
| join | Client → Server | Join a room |
| send_message | Client → Server | Send a message |
| leave | Client → Server | Leave a room |
| user_joined | Server → Client | Someone joined |
| new_message | Server → Client | New message received |
| user_left | Server → Client | Someone left |

## Run Locally

```bash
git clone https://github.com/AmanShrestha-01/Chat-App.git
cd Chat-App
pip install -r requirements.txt
python app.py
```

Visit API docs: http://127.0.0.1:8000/apidocs

## Run Tests

```bash
python test_app.py
```
