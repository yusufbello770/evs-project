from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Election, Candidate, Vote

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('main.register'))

        user = User(username=username, email=email, password=password, role='voter')
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully.')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid login.')
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    elections = Election.query.all()
    return render_template('dashboard.html', elections=elections)

@main.route('/vote/<int:election_id>', methods=['GET', 'POST'])
@login_required
def vote(election_id):
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    if request.method == 'POST':
        candidate_id = request.form['candidate']
        existing_vote = Vote.query.filter_by(voter_id=current_user.user_id, candidate_id=candidate_id).first()
        if existing_vote:
            flash('You already voted.')
        else:
            vote = Vote(voter_id=current_user.user_id, candidate_id=candidate_id)
            db.session.add(vote)
            db.session.commit()
            flash('Vote cast successfully.')
        return redirect(url_for('main.dashboard'))
    return render_template('vote.html', candidates=candidates)

@main.route('/results/<int:election_id>')
@login_required
def results(election_id):
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    data = []
    labels = []
    for candidate in candidates:
        labels.append(candidate.name)
        count = Vote.query.filter_by(candidate_id=candidate.candidate_id).count()
        data.append(count)
    return render_template('results.html', labels=labels, data=data)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))