from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, TestResult
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
import sounddevice as sd

a0 = 1e-5 
sr = 44100 
userResult=TestResult()
def sinusoid(d, f, phi, l, a0=a0, sr=sr):
    t = np.arange(0, int(round(d * sr))) / sr
    return a0 * 10 ** (l / 20) * np.sin(2 * np.pi * f * t + phi)


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/playtone250", methods=['GET', 'POST'])
def playtone250():
    if request.method == 'POST':
        dbLevel = request.form.get('dbLevel')
        heard = request.form.get('heard')
        if dbLevel:
            tone = sinusoid(1, 250, 0, float(dbLevel))
            sd.play(tone, sr)
            sd.wait()
        if heard:
            userResult.f250db = float(heard)
            userResult.user_id = current_user.id
            db.session.add(userResult)
            db.session.commit()
            flash('Hearing test result for 250 Hz saved!', 'success')
            return redirect(url_for('playtone500'))
    return render_template('f250.html')

@app.route("/playtone500", methods=['GET', 'POST'])
def playtone500():
    if request.method == 'POST':
        dbLevel = request.form.get('dbLevel')
        heard = request.form.get('heard')
        if dbLevel:
            tone = sinusoid(1, 500, 0, float(dbLevel))
            sd.play(tone, sr)
            sd.wait()
        if heard:
            userResult.f500db = float(heard)
            userResult.user_id = current_user.id
            db.session.add(userResult)
            db.session.commit()
            flash('Hearing test result saved!', 'success')
            return redirect(url_for('playtone1000'))
    return render_template('f500.html')

@app.route("/playtone1000", methods=['GET', 'POST'])
def playtone1000():
    if request.method == 'POST':
        dbLevel = request.form.get('dbLevel')
        heard = request.form.get('heard')
        if dbLevel:
            tone = sinusoid(1, 1000, 0, float(dbLevel))
            sd.play(tone, sr)
            sd.wait()
        if heard:
            userResult.f1000db = float(heard)
            userResult.user_id = current_user.id
            db.session.add(userResult)
            db.session.commit()
            flash('Hearing test result saved!', 'success')
            return redirect(url_for('playtone2000'))
    return render_template('f1000.html')


@app.route("/playtone2000", methods=['GET', 'POST'])
def playtone2000():
    if request.method == 'POST':
        dbLevel = request.form.get('dbLevel')
        heard = request.form.get('heard')
        if dbLevel:
            tone = sinusoid(1, 2000, 0, float(dbLevel))
            sd.play(tone, sr)
            sd.wait()
        if heard:
            userResult.f2000db = float(heard)
            userResult.user_id = current_user.id
            db.session.add(userResult)
            db.session.commit()
            flash('Hearing test result saved!', 'success')
            return redirect(url_for('playtone4000'))
    return render_template('f2000.html')

@app.route("/playtone4000", methods=['GET', 'POST'])
def playtone4000():
    if request.method == 'POST':
        dbLevel = request.form.get('dbLevel')
        heard = request.form.get('heard')
        if dbLevel:
            tone = sinusoid(1, 4000, 0, float(dbLevel))
            sd.play(tone, sr)
            sd.wait()
        if heard:
            userResult.f4000db = float(heard)
            userResult.user_id = current_user.id
            db.session.add(userResult)
            db.session.commit()
            flash('Hearing test result saved!', 'success')
            return redirect(url_for('playtone8000'))
    return render_template('f4000.html')

@app.route("/playtone8000", methods=['GET', 'POST'])
def playtone8000():
    if request.method == 'POST':
        dbLevel = request.form.get('dbLevel')
        heard = request.form.get('heard')
        if dbLevel:
            tone = sinusoid(1, 8000, 0, float(dbLevel))
            sd.play(tone, sr)
            sd.wait()
        if heard:
            userResult.f8000db = float(heard)
            userResult.user_id = current_user.id
            db.session.add(userResult)
            db.session.commit()
            flash('Hearing test result saved!', 'success')
            return redirect(url_for('about'))
    return render_template('f8000.html')

@app.route("/result", methods=['GET', 'POST'])
def result():
     return render_template('about.html', title='About')

@app.route("/", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')