from flask import Flask, jsonify
from models import db
from auth.routes import auth_bp, bcrypt
from chat.routes import chat_bp
from events import socketio
from flasgger import Swagger

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SECRET_KEY"] = "your-secret-key-change-this-later"
app.config["SWAGGER"] = {
    "title": "Chat App API",
    "description": "A real-time chat API with rooms, messaging, and WebSockets",
    "version": "1.0.0"
}

db.init_app(app)
bcrypt.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")

swagger = Swagger(app)

app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Chat App API is running"})

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8000)
