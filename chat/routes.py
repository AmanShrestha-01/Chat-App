from flask import Blueprint, jsonify, request
from models import db, Room, Message
from middleware import get_logged_in_user
import datetime

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/rooms", methods=["POST"])
def create_room():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Room name is required"}), 400
    existing = Room.query.filter_by(name=data["name"]).first()
    if existing:
        return jsonify({"error": "Room already exists"}), 409
    room = Room(name=data["name"], created_by=user["user_id"])
    db.session.add(room)
    db.session.commit()
    return jsonify({"id": room.id, "name": room.name}), 201

@chat_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()
    result = []
    for r in rooms:
        result.append({"id": r.id, "name": r.name})
    return jsonify(result)

@chat_bp.route("/rooms/<int:room_id>/messages", methods=["GET"])
def get_messages(room_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    messages = Message.query.filter_by(room_id=room_id).all()
    result = []
    for m in messages:
        result.append({
            "id": m.id,
            "username": m.username,
            "content": m.content,
            "created_at": m.created_at
        })
    return jsonify(result)
