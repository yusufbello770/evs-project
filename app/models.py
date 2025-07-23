from . import db
from flask_login import UserMixin
from app import login_manager

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))

    def get_id(self):
        return str(self.user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Election(db.Model):
    election_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(20))

class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    election_id = db.Column(db.Integer, db.ForeignKey('election.election_id'))

class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.candidate_id'))