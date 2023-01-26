from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)



class UserProject(db.Model):
    """People assigned to a project"""

    __tablename__ = 'user_projects'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True,)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="CASCADE"), primary_key=True,)

class User(db.Model):
    """User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.Text, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    full_name = db.Column(db.Text, nullable = False)
    assigments = db.relationship(
        "User",
        secondary="user_projects",
        primaryjoin=(UserProject.user_id == id)
    )

    @classmethod
    def register(cls, username, password, email, full_name,):
        """Register user with hashed password, return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        user = cls(
            username=username, 
            password=hashed_utf8,
            email=email,
            full_name=full_name,
        )

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Verify that the user is who they say they are by 
        checking input against hashed password, then return user"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False    

class Project(db.Model):
    """A project"""

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    assignments = db.relationship('UserProject', backref='project')
    messages = db.relationship('Message')
    todos = db.relationship('Todo')
    # todos = db.relationship('ProjectTodos', backref='project')



class Todo(db.Model):
    """A todo for a certain project"""

    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(250))
    project_id = db.Column(db.ForeignKey('project.id', ondelete="cascade"))
    project = db.relationship('Project')


class Message(db.Model):
    """Messages for a project"""

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    from_user = db.Column(db.String(100), nullable= False)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(),)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="cascade"))

class Team(db.Model):
    """Users on your team."""

    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
