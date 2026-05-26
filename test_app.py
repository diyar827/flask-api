import pytest
from app import app, db, Charger, Session, Invoice

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_chargers(client):
    response = client.get('/chargers/')
    assert response.status_code == 200

def test_get_sessions(client):
    response = client.get('/sessions/')
    assert response.status_code == 200

def test_get_billing(client):
    response = client.get('/billing/')
    assert response.status_code == 200

def test_post_charger(client):
    response = client.post('/chargers/', json={
        "location": "Test By",
        "status": "available",
        "power_kw": 22.0
    })
    assert response.status_code == 201

def test_post_session(client):
    # Opret først en charger
    client.post('/chargers/', json={
        "location": "Test By",
        "status": "available",
        "power_kw": 22.0
    })
    response = client.post('/sessions/', json={
        "charger_id": 1,
        "user_id": "test_user",
        "energy_kwh": 10.0,
        "status": "completed"
    })
    assert response.status_code == 201

def test_analytics_summary(client):
    response = client.get('/analytics/summary')
    assert response.status_code == 200

def test_anomaly_detection(client):
    # Opret først en charger
    client.post('/chargers/', json={
        "location": "Test By",
        "status": "occupied",
        "power_kw": 22.0
    })
    response = client.get('/maintenance/anomaly/1')
    assert response.status_code == 200