import json
from app import app, db

def get_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.app_context():
        db.create_all()
    return app.test_client()

def get_token(client):
    client.post("/signup",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json"
    )
    response = client.post("/login",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)
    return data["token"]

def test_home():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200
    print("PASS: Home route works")

def test_signup():
    client = get_client()
    response = client.post("/signup",
        data=json.dumps({"username": "newuser", "password": "pass123"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    print("PASS: Signup works")

def test_login():
    client = get_client()
    client.post("/signup",
        data=json.dumps({"username": "loginuser", "password": "pass123"}),
        content_type="application/json"
    )
    response = client.post("/login",
        data=json.dumps({"username": "loginuser", "password": "pass123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "token" in data
    print("PASS: Login works")

def test_create_room():
    client = get_client()
    token = get_token(client)
    response = client.post("/rooms",
        data=json.dumps({"name": "test-room"}),
        content_type="application/json",
        headers={"Authorization": token}
    )
    assert response.status_code == 201
    print("PASS: Room creation works")

def test_list_rooms():
    client = get_client()
    response = client.get("/rooms")
    assert response.status_code == 200
    print("PASS: List rooms works")

def test_messages_require_login():
    client = get_client()
    response = client.get("/rooms/1/messages")
    assert response.status_code == 401
    print("PASS: Messages reject unauthenticated users")

if __name__ == "__main__":
    test_home()
    test_signup()
    test_login()
    test_create_room()
    test_list_rooms()
    test_messages_require_login()
    print("\nAll tests passed!")
