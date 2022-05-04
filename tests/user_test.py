"""User action test"""
import os
from pathlib import Path

from app.db.models import User


def test_user_register(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
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
        'email': "test@test.com",
        'password': "testtest",
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
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root / 'tests' / 'test_transactions.csv'
    upload_dir = root / 'app' / 'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file, 'rb')
    }
    client.post('/transactions/upload', data=data)
    assert len(os.listdir(upload_dir)) == 1
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/' + file)


def test_user_to_transaction_relationship(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root / 'tests' / 'test_transactions.csv'
    upload_dir = root / 'app' / 'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file, 'rb')
    }
    client.post('/transactions/upload', data=data)
    assert len(os.listdir(upload_dir)) == 1
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/' + file)
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
        'email': "test1@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    response = client.get('/transactions')
    assert b'DEBIT' not in response.data


def test_user_upload_wrong_file_type(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root / 'tests' / 'test.txt'
    upload_dir = root / 'app' / 'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file, 'rb')
    }
    response = client.post('/transactions/upload', data=data)
    assert b'csv file only' in response.data
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/' + file)


def test_user_upload_wrong_file_content(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root / 'tests' / 'test_wrong_transactions.csv'
    upload_dir = root / 'app' / 'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file, 'rb')
    }
    client.post('/transactions/upload', data=data)
    response = client.get('/transactions/upload')
    assert b'please check the content of your file' in response.data
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/' + file)


def test_user_upload_multiple_file(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root / 'tests' / 'test_transactions.csv'
    test_file1 = root / 'tests' / 'test_transactions1.csv'
    upload_dir = root / 'app' / 'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    # post first file
    data = {
        'file': open(test_file, 'rb')
    }
    client.post('/transactions/upload', data=data)
    # post second file
    data = {
        'file': open(test_file1, 'rb')
    }
    client.post('/transactions/upload', data=data)
    # get current user from database
    current_user = User.query.filter_by(email='test@test.com').first()
    assert len(current_user.transaction) == 56
    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/' + file)

def test_user_balance(client):
    data = {
        'email': "test@test.com",
        'password': "testtest",
        'confirm': "testtest"
    }
    client.post('/register', data=data)
    data = {
        'email': "test@test.com",
        'password': "testtest",
    }
    client.post('/login', data=data)
    root = Path(__file__).parent.parent
    test_file = root / 'tests' / 'test_transactions.csv'
    upload_dir = root / 'app' / 'uploads'
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    if len(os.listdir(upload_dir)) != 0:
        for file in os.listdir(upload_dir):
            os.remove(str(upload_dir) + '/' + file)
    assert len(os.listdir(upload_dir)) == 0
    data = {
        'file': open(test_file, 'rb')
    }
    client.post('/transactions/upload', data=data)
    # get current user from database
    current_user = User.query.filter_by(email='test@test.com').first()
    balance = 0
    for t in current_user.transaction:
        balance += t.amount
    assert balance == current_user.balance

    for file in os.listdir(upload_dir):
        os.remove(str(upload_dir) + '/' + file)