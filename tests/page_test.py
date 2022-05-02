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

def test_request_page_not_found(client):
    """This makes the index page"""
    response = client.get("/page5")
    assert response.status_code == 404

def test_requset_page_redirect(client):
    response = client.get("/dashboard")
    assert response.status_code == 302