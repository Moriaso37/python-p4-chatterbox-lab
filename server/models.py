import unittest
from app import create_app
from models import db, Message

class MessageModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_message_model(self):
        with self.app.app_context():
            msg = Message(body="Hi", username="Test")
            db.session.add(msg)
            db.session.commit()
            self.assertEqual(Message.query.count(), 1)
