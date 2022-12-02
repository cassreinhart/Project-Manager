"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///projectmanager-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(
            text="Message",
            timestamp="now",
            user_id=1
        )

        db.session.add(m)
        db.session.commit()

        # Message should have this text & user_id of 1
        self.assertEqual(m.text, "Message")
        self.assertEqual(m.user_id), 1)