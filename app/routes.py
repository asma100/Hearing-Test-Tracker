from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, TestResult,LTestvalue,RTestvalue
from flask_login import login_user, current_user, logout_user, login_required
from app.createdFunction import evaluate_hearing, handle_playtone_request,evaluate_hearing_o

import sounddevice as sd

a0 = 1e-5 
sr = 44100 

@app.route("/home",methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('settings'))
    return render_template('home.html')

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', title='About')

@app.route("/rightLeft", methods=['GET', 'POST'])
def rightLeft():
    if request.method == 'POST':
        ear = request.form.get('ear')
        test_result = TestResult(ear=ear, user_id=current_user.id)
        db.session.add(test_result)
        db.session.commit()
        return redirect(url_for('playtone250'))
    return render_template('rightLeft.html')

@app.route("/playtone250", methods=['GET', 'POST'])
def playtone250():
    if request.method == 'POST':
        heard = handle_playtone_request(request, 250)
        if heard:
            return redirect(url_for('playtone500'))
    return render_template('f250.html')

@app.route("/playtone500", methods=['GET', 'POST'])
def playtone500():
    if request.method == 'POST':
        heard = handle_playtone_request(request, 500)
        if heard:
            return redirect(url_for('playtone1000'))
    return render_template('f500.html')

@app.route("/playtone1000", methods=['GET', 'POST'])
def playtone1000():
    if request.method == 'POST':
        heard = handle_playtone_request(request, 1000)
        if heard:
            return redirect(url_for('playtone2000'))
    return render_template('f1000.html')

@app.route("/playtone2000", methods=['GET', 'POST'])
def playtone2000():
    if request.method == 'POST':
        heard = handle_playtone_request(request, 2000)
        if heard:
            return redirect(url_for('playtone4000'))
    return render_template('f2000.html')

@app.route("/playtone4000", methods=['GET', 'POST'])
def playtone4000():
    if request.method == 'POST':
        heard = handle_playtone_request(request, 4000)
        if heard:
            return redirect(url_for('playtone8000'))
    return render_template('f4000.html')

@app.route("/playtone8000", methods=['GET', 'POST'])
def playtone8000():
    if request.method == 'POST':
        heard = handle_playtone_request(request, 8000)
        if heard:
            # Retrieve the user result
            userEar = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.id.desc()).first()
            if userEar.ear == 'left':
                userResult = LTestvalue.query.filter_by(user_id=current_user.id).order_by(LTestvalue.id.desc()).first()
            elif userEar.ear == 'right':
                userResult = RTestvalue.query.filter_by(user_id=current_user.id).order_by(RTestvalue.id.desc()).first()

            results, overall_assessment = evaluate_hearing(userResult)
            
            # Save the overall assessment and results into the TestResult object
            test_result = TestResult.query.filter_by(user_id=current_user.id, ear=userEar.ear).order_by(TestResult.id.desc()).first()
            test_result.overall_assessment = overall_assessment
            test_result.f250db = results['f250db']
            test_result.f500db = results['f500db']
            test_result.f1000db = results['f1000db']
            test_result.f2000db = results['f2000db']
            test_result.f4000db = results['f4000db']
            test_result.f8000db = results['f8000db']
            db.session.commit()

            return redirect(url_for('result', overall_assessment=overall_assessment, **results))
    return render_template('f8000.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    overall_assessment = request.args.get('overall_assessment')
    results = {
        'f250db': request.args.get('f250db'),
        'f500db': request.args.get('f500db'),
        'f1000db': request.args.get('f1000db'),
        'f2000db': request.args.get('f2000db'),
        'f4000db': request.args.get('f4000db'),
        'f8000db': request.args.get('f8000db')
    }
    return render_template('result.html', title='Result', overall_assessment=overall_assessment, results=results)

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
    results = TestResult.query.filter_by(user_id=current_user.id).all()
    user = User.query.get(current_user.id).username
    return render_template('account.html', title='Account',results=results, user=user)

#@app.route("/history")
#@login_required
#def history():
  #  results = TestResult.query.filter_by(user_id=current_user.id).all()
  
 #  return render_template('history.html', results=results)

   
