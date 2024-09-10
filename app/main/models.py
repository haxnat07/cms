from app.extensions import db
from app.auth.models import User



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    tasks = db.relationship('Task', backref='project', lazy=True)


# Association table for Task and User (many-to-many relationship)
task_user = db.Table('task_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    users = db.relationship('User', secondary='task_user', backref='tasks')
    