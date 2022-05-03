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


def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/about"' in response.data
    assert b'href="/welcome"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data


def test_main_menu_links_without_user_login(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/dashboard"' not in response.data
    assert b'href="/transactions"' not in response.data
    assert b'href="/transactions/upload"' not in response.data


def test_main_menu_links_with_user_login(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data1 = {
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data1)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'href="/dashboard"' in response.data
    assert b'href="/transactions"' in response.data
    assert b'href="/transactions/upload"' in response.data
