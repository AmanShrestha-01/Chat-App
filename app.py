from flask import Flask, jsonify
from models import db
from auth.routes import auth_bp, bcrypt
from chat.routes import chat_bp
from events import socketio

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SECRET_KEY"] = "your-secret-key-change-this-later"

db.init_app(app)
bcrypt.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Chat App API is running"})

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8000)
