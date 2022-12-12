from flask import Flask, session, render_template, redirect, flash, jsonify, url_for, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from authlib.integrations.flask_client import OAuth

from forms import ProjectForm, RegisterForm, TodoForm, AssignmentForm, MessageForm, LoginForm
from models import db, connect_db, User, Project, UserProject, Message, Todo
from sqlalchemy.exc import IntegrityError

# from dotenv import auth_uri

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///projectstest"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#Best way to configure client_id and client_secret


app.config['GOOGLE_AUTHORIZE_URL'] = "https://accounts.google.com/o/oauth2/auth"
app.config['GOOGLE_ACCESS_TOKEN_URL'] = "https://oauth2.googleapis.com/token"
app.config['GOOGLE_API_BASE_URL'] = "https://www.googleapis.com/calendar/v3"


connect_db(app)

toolbar = DebugToolbarExtension(app)

oauth = OAuth(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#### use authlib or google auth oauthlib for Oauth2??? #######
# google = oauth.register('google', {
#     'api_base_url':'https://www.googleapis.com/calendar/v3',
#     'server_metadata_url':'https://accounts.google.com/.well-known/openid-configuration',
#     'client_kwargs':{'scope': 'openid calendar'},
# })

# @app.route('/login')
# def login():
#     redirect_uri = url_for('authorize', _external=True)
#     return google.authorize_redirect(redirect_uri, auth_uri)

# @app.route('/authorize')
# def authorize():
#     token = google.authorize_access_token()
#     # you can save the token into database
#     profile = google.get('/user', token=token)
#     return jsonify(profile)


@app.route('/')
def index():

    if g.user:
        project_ids = [p.id for p in g.user.assigments]

        messages = (Message
                    .query
                    .filter(Message.project_id.in_(project_ids))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())

        return render_template('index.html', messages=messages)

    else:
        return redirect('/user/register')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


#################### PEOPLE VIEWS ##############################

@app.route('/user/register', methods=['GET', 'POST'])
def register_user():
    """Create new person to assign to projects."""
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                full_name=form.full_name.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    return render_template('/users/signup.html', form = form)

#################### PROJECT VIEWS ##############################

@app.route('/projects', methods=['GET', 'POST'])
def all_projects():
    """show all projects with a form for adding new projects. Handle add project form."""
    projects = Project.query.all()

    form = ProjectForm()

    if form.validate_on_submit():
        name = form.data.name
        description = form.data.description
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()

        return redirect(f'/project/{project_id}')

    return render_template('/project/projects.html', projects = projects, form = form)

@app.route('/projects/<int:project_id>')
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    todos = Todo.query.get(project_id)

    return render_template('/project/detail.html', project=project, todos = todos)

@app.route('/projects/<int:project_id>/assignments')
def show_assignments(project_id):
    project = Project.query.get(project_id)
    people = project.assignments

    return render_template('/project/assignments.html', people = people, project = project)

@app.route('/projects/<int:project_id>/assignments/add', methods=['GET', 'POST'])
def add_assignments(project_id):
    project = Project.query.get(project_id)
    
    form = AssignmentForm()

    projects = [(p.id, p.name) for p in Project.query.all()]
    form.project.choices = projects

    people = [(p.id, p.name) for p in People.query.all()]
    form.person.choices = people

    if form.validate_on_submit():
        person = form.data.people_id ################ How to grab data from select field-- see handle_message_form
        assignment = PeopleProject(project_id = project_id, people_id = person.id) ### just pass in person id???
        db.session.add(assignment)
        db.session.commit()
        return redirect(f'/projects/{project_id}/assigments')

    return render_template('/project/add_assignee.html', project = project, form = form)

@app.route('/project/<int:project_id>/add-todo', methods=['GET', 'POST'])
def add_todo_to_project(project_id):
    form = TodoForm()

    projects = [(p.id, p.name) for p in Project.query.all()]
    form.project.choices = projects

    if form.validate_on_submit():
        print(form.data)
        name = form.data.name
        print(name)
        detail = form.data.detail
        project_id = form.data.project_id
        new_todo = Todo(name=name, detail=detail, project_id = project_id)

        db.session.add(new_todo)
        db.session.commit()
        return redirect(f'project/{project_id}')
    
    return render_template('/project/add_todo.html', form = form)


#################### MESSAGE VIEWS ##############################

@app.route('/message', methods=['GET', 'POST'])
def send_message():
    """Send Messages"""
    ### see handle_message_form
    form = MessageForm()

    projects = [(p.id, p.name) for p in Project.query.all()]
    form.project.choices = projects

    if form.validate_on_submit():
        from_user = form.data.from_user
        title = form.data.title
        content = form.data.content
        project_id = form.data.project_id
        new_message = Message(title=title, content=content, project_id=project_id)
        db.session.add(new_message)
        db.session.commit()
        return redirect(f'/project/{project_id}')
    return render_template('/message/add.html', form = form)
