from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)


class People(db.Model):
    """A person working on projects and tasks."""

    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    

class Project(db.Model):
    """A project"""

    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)
    assignments = db.relationship('UserProject', backref='project')
    todos = db.relationship('Todo')
    # todos = db.relationship('ProjectTodos', backref='project')

class Todo(db.Model):
    """A todo for a certain project"""

    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(250))
    project_id = db.Column(db.ForeignKey('project.id'))
    project = db.relationship('Project')

# class ProjectTodos(db.Model):
#     """People assigned to a project"""

#     __tablename__ = 'project_todos'

#     todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'), primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)

class UserProject(db.Model):
    """People assigned to a project"""

    __tablename__ = 'user_projects'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)


class Message(db.Model):
    """Messages for a project"""

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    from_user = db.Column(db.String(100), nullable= False)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class User(db.Model):
    """User."""

    __tablename__ = 'users'

    username = db.Column(db.Text, primary_key = True, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    full_name = db.Column(db.Text, nullable = False)
    assignments = db.relationship('UserProject', backref='user')

    @classmethod
    def register(cls, username, pwd, email, full_name,):
        """Register user with hashed password, return user"""

        hashed = bcrypt.generate_password_hash(pwd)
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