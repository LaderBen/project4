"""This is home page test"""

def test_request_homepage_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'Index Page' in response.data

def test_request_welcomepage_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_request_about_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'About' in response.data
