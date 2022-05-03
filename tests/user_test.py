"""User action test"""
import os
from pathlib import Path

from app.db.models import User

def test_user_register(client):
    data = {
        'email' : "test@test.com",
        'password' : "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    user = User.query.filter_by(email='test@test.com').first()
    assert user.email == 'test@test.com'

def test_user_login(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email' : "test@test.com",
        'password' : "testtest",
    }
    client.post('/login', data=data)
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_user_file_upload(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email' : "test@test.com",
        'password' : "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root/'tests'/'test_transactions.csv'
    upload_dir = root/'app'/'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file,'rb')
    }
    client.post('/transactions/upload', data=data)
    assert len(os.listdir(upload_dir)) == 1
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/'+file)

def test_user_to_transaction_relationship(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email' : "test@test.com",
        'password' : "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root/'tests'/'test_transactions.csv'
    upload_dir = root/'app'/'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file,'rb')
    }
    client.post('/transactions/upload', data=data)
    assert len(os.listdir(upload_dir)) == 1
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/'+file)
    response = client.get('/transactions')
    assert b'DEBIT' in response.data
    # logout current user
    client.get('/logout')
    # register a new user and login
    data = {
        'email': "test1@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email' : "test1@test.com",
        'password' : "testtest",
    }
    client.post('/login', data=data)
    response = client.get('/transactions')
    assert b'DEBIT' not in response.data
