from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User  # Ensure models.py has db and User
from models import CareerGoal, Skill, Resource
from functools import wraps
from flask import redirect, url_for, session, flash
from models import UserProgress


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goalglow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name  # so we can greet them
            flash("Login successful!")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        flash("Signup successful!")
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to log in first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    goals = CareerGoal.query.all()
    skill_gap = None
    roadmap = None
    career_goal_name = None

    # Get defaults from session
    current_skills = session.get("current_skills", "")
    career_goal_id = session.get("career_goal_id", "")

    user_id = session["user_id"]

    # Handle marking skill as completed
    if request.method == "POST" and "complete_skill" in request.form:
        skill_to_complete = request.form.get("complete_skill")
        goal_id = session.get("career_goal_id")
        if skill_to_complete and goal_id:
            progress = UserProgress.query.filter_by(
                user_id=user_id, goal_id=goal_id, skill_name=skill_to_complete
            ).first()
            if not progress:
                progress = UserProgress(
                    user_id=user_id, goal_id=goal_id, skill_name=skill_to_complete, completed=True
                )
                db.session.add(progress)
            else:
                progress.completed = True
            db.session.commit()

    if request.method == "POST" and "generate_roadmap" in request.form:
        current_skills = request.form.get("current_skills", "")
        career_goal_id = request.form.get("career_goal", "")

        # Save to session for stability
        session["current_skills"] = current_skills
        session["career_goal_id"] = career_goal_id

    skills_list = [skill.strip().lower() for skill in current_skills.split(",") if skill.strip()]
    completed_skills = []
    progress_percent = 0

    if career_goal_id:
        goal = CareerGoal.query.get(career_goal_id)
        career_goal_name = goal.name
        required_skills = [s.name.lower() for s in goal.skills]
        skill_gap = [s for s in required_skills if s not in skills_list]

        # Get completed skills from UserProgress
        completed_progress = UserProgress.query.filter_by(
            user_id=user_id, goal_id=career_goal_id, completed=True
        ).all()
        completed_skills = [p.skill_name for p in completed_progress]

        # Calculate progress
        total = len(required_skills)
        done = len([s for s in required_skills if s in completed_skills or s in skills_list])
        progress_percent = int((done / total) * 100) if total > 0 else 0

        roadmap = []
        for skill in skill_gap:
            roadmap.append({
                "skill": skill.capitalize(),
                "completed": skill in completed_skills,
                "resources": [
                    ("W3Schools", f"https://www.w3schools.com/{skill}"),
                    ("FreeCodeCamp", "https://www.freecodecamp.org/learn"),
                    ("Codecademy", f"https://www.codecademy.com/catalog/language/{skill}"),
                    ("SoloLearn", f"https://www.sololearn.com/en/learn/{skill}"),
                    ("MDN Web Docs", f"https://developer.mozilla.org/en-US/docs/Web/{skill}"),
                    ("GeeksforGeeks", f"https://www.geeksforgeeks.org/{skill}"),
                    ("TutorialsPoint", f"https://www.tutorialspoint.com/{skill}/index.htm"),
                    ("The Odin Project", "https://www.theodinproject.com"),
                    ("Scrimba", "https://scrimba.com"),
                    ("Educative.io", "https://www.educative.io")
                ]
            })

    return render_template(
        "dashboard.html",
        goals=goals,
        skill_gap=skill_gap,
        career_goal_name=career_goal_name,
        roadmap=roadmap,
        user_name=session.get("user_name"),
        current_skills=current_skills,
        career_goal_id=career_goal_id,
        completed_skills=completed_skills,
        progress_percent=progress_percent
    )


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('login'))

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    