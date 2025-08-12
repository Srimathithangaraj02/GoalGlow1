from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class CareerGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    skills = db.relationship('Skill', backref='career_goal', lazy=True)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    career_goal_id = db.Column(db.Integer, db.ForeignKey('career_goal.id'), nullable=False)
    resources = db.relationship('Resource', backref='skill', lazy=True)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300), nullable=False)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('career_goal.id'))
    skill_name = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)