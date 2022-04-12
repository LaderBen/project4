"""This is home page test"""

def test_requst_homepage_content(client):
    response = client.get("/")
    assert response.staus_code == 200
    assert b'Hello, World!' in response.data