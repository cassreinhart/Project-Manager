# Project-Manager
Springboard Bootcamp Capstone 1 using Python / Flask / Postgres. This site is intended to serve teams collaborating on projects to reach their goals. 

## Features: 
- Easily invite your teammates to join (critical to gain access to team projects and collaboration).
- Secure access to your projects.
- Includes a team messaging feature, adding additional communication for team reminders/updates.
- Full CRUD for project and task creation to ensure you can easily manage details.
- Implemented with Google Calendar API for added calendar management.

## User Flow: 
- Login/Register view contains forms to sign up or sign in.
- Upon login, the home page loads a screen with easy navigation to projects, inviting collaborators, and Calendar/Messages at a glance.
- On projects tab, navigate to the project you are interested in, or create a new project.
- From the project details, you can easily manage tasks and project collaborators
- From the invite page, enter email addresses to invite users to join the Project Management App.

---
## 1. Set Up Virtual Environment
After cloning the repo, you will need to set up a virtual environment and install dependencies for the application to run locally.
- In the local repository, use `pip install -r requirements.txt` to install dependencies.
- Ensure you have Postgres up and running locally. Then enter `createdb projectstest` to create the database.

## 2. Run Development Site
To view your changes to the code and test out the site, use the commands below or visit the deployment site at bottom.
- Use `FLASK_ENV=development flask run` to run on port 5000.
- Visit [localhost](https://localhost:5000) to navigate to development site.

### See the Deployed Site at [Project Manager](google.com)