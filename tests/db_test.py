from app import db
from app.db.models import User, Transaction

def test_add_user(application):
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        user = User('test@test.com','testtest')
        db.session.add(user)
        user = User.query.filter_by(email='test@test.com').first()
        assert user.password == 'testtest'
        assert db.session.query(User).count() == 1

def test_add_transaction(application):
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        user = User('test@test.com','testtest')
        db.session.add(user)
        user.transaction = [Transaction(200,'DEBIT'),Transaction(300,'CREDIT')]
        assert db.session.query(Transaction).count() == 2

def test_modify_transaction(application):
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Transaction).count() == 0
        user = User('test@test.com','testtest')
        db.session.add(user)
        user.transaction = [Transaction(200,'DEBIT'),Transaction(300,'CREDIT')]
        t1 = Transaction.query.filter_by(type='DEBIT').first()
        assert t1.amount == 200
        t1.amount = 400
        db.session.commit()
        t1 = Transaction.query.filter_by(type='DEBIT').first()
        assert t1.amount == 400

