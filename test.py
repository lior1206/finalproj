import pytest
import mongomock
import bcrypt
from app import create_app

@pytest.fixture
def app(monkeypatch):
    # Use mongomock for MongoDB connection
    mock_client = mongomock.MongoClient()
    mock_db = mock_client.finaldb

    # Create the Flask app with the test config
    test_config = {
        'TESTING': True,
        'MONGO_CLIENT': mock_client
    }
    app = create_app(test_config)
    
    # Override the app's MongoDB database with our mock database
    monkeypatch.setattr(app, "db", mock_db)
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_db(app):
    with app.app_context():
        app.db.users_auth.insert_one({
            'username': 'testuser',
            'password': bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()),
            'email': 'testuser@example.com'
        })
        yield
        app.db.client.drop_database('finaldb')

def test_db_connection(client):
    # No need for `app` fixture here, using `client` directly
    response = client.get('/')
    assert response.status_code == 200

def test_insert_user(client, setup_db):
    response = client.post('/signup', data={
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 302  # Redirect to /calc
    user = client.application.db.users_auth.find_one({'username': 'newuser'})
    assert user is not None
    assert user['email'] == 'newuser@example.com'

def test_login_success(client, setup_db):
    response = client.post('/', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Redirect to /calc

def test_login_failure(client, setup_db):
    response = client.post('/', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401  # Unauthorized
    assert b"Incorrect password" in response.data
