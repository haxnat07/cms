from flask import render_template, redirect, url_for, flash, request
from app.auth import auth_bp
from app.extensions import db
from app.auth.models import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.forms import RegistrationForm, LoginForm




@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not name or len(name) < 2 or len(name) > 150:
            flash("Name must be between 2 and 150 characters.", "danger")
        elif not password or len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
        elif password != confirm_password:
            flash("Passwords must match.", "danger")
        else:
            # Check if email already exists
            existing_user = User.query.filter_by(name=name).first()
            if existing_user:
                flash("Username is already in use. Please choose a different one.", "danger")
            else:
                # All validations passed, create the user
                hashed_password = generate_password_hash(password)
                user = User(name=name, password=hashed_password)
                user.points = 100
                db.session.add(user)
                try:
                    db.session.commit()
                    flash('Your account has been created! You can now log in.', 'success')
                    print('Your account has been created! You can now log in.')
                    return redirect(url_for('auth.login'))
                except Exception as e:
                    db.session.rollback()  # Rollback the session in case of IntegrityError
                    flash(f"An error occurred while creating your account. Please try again. Error: {str(e)}", "danger")

    return render_template('register.html')




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Basic validation
        if not password:
            flash("Password is required.", "danger")
        else:
            user = User.query.filter_by(name=name).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))