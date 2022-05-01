def test_request_main_menu_links(client):
    """Test the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_page(client):
    """Test the auth page"""
    response = client.get("/dashboard")
    assert response.status_code == 302

def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
