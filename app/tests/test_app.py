from flask_login import logout_user
import pytest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        

def test_index(client):
	response = client.get('/')
	assert response.status_code == 200
 
def test_signup(client):
	response = client.get('/signup')
	assert response.status_code == 200

def test_profile_without_login(client):
	response = client.get('/profile')
	assert response.status_code == 302

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
 
def test_with_login(client):
    good_email = 'user@example.com'
    good_password = '123456'
    client.post('/login', data={'email' : good_email, 'password' : good_password})
    response = client.get('/profile')
    assert response.status_code == 200
    
def test_logout_logged_in(client):
    email = 'user@example.com'
    password = '123456'
    client.post('/login', data={'email' : email, 'password' : password})
    response = client.get('/logout')
    assert response.status_code == 302

def test_logout_logged_out(client):
    response = client.get('/logout')
    assert response.status_code == 302