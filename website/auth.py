import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from .models import User
from . import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', 'error')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('E-posta adresi veya şifre yanlış.', 'error')

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', 'error')
            return redirect(url_for('auth.signup'))

        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[A-Z]", password):
            flash('Password must be at least 8 characters long, include a number and an uppercase letter.', 'error')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This Email address is already associated with an account.', 'warning')
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(name=name, surname=surname, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered! You can log in now.', 'success')
            return redirect(url_for('auth.login'))
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')

    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have signed out successfully.', 'success')
    return redirect(url_for('views.home'))
