import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client   

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def test_index(client, driver):
    driver.get('http://tutoflaskauth.azurewebsites.net/')
    response = client.get('/')
    assert driver.title == "Flask auth app"
    assert response.status_code == 200
    driver.close()
 
def test_signup(client, driver):
    driver.get('http://tutoflaskauth.azurewebsites.net/signup')
    response = client.get('/signup')
    h3_title = driver.find_element(By.CLASS_NAME, "title")
    assert h3_title.text == "Sign Up"
    assert response.status_code == 200
    driver.close()

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