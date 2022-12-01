from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Email, Length

class MessageForm(FlaskForm):
    """Form for sending a message to the team"""

    from_user = StringField("From", validators=[InputRequired()])
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Message")
    project = SelectField("Project", coerce=int)

class TodoForm(FlaskForm):
    """Form for adding a todo to a project"""

    name = StringField("Name", validators=[InputRequired()])
    detail = TextAreaField("Detail")
    project = SelectField("Project", coerce=int)
    
class ProjectForm(FlaskForm):
    """Form for adding a new Project"""

    name = StringField("Project Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])

class PeopleForm(FlaskForm):
    """Form for adding a new Person"""

    name = StringField("Name", validators=[InputRequired()])
    email = EmailField("Gmail", validators=[InputRequired(), Email()])

class AssignmentForm(FlaskForm):
    """Form for assigning People to a Project"""

    person = SelectField("Person", coerce=int)
    project = SelectField("Project", coerce=int)








class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username= StringField("Username", validators=[InputRequired(), Length(min = 6, max = 20)])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField("Repeat Password")
    email = EmailField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])