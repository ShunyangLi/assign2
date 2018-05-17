from server import app
from datetime import datetime
from EventSystem import Eventsystem
from event import User, Event,db
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def index():
    now = datetime.now()
    for event in Event.query.all():
        if event.end < str(now):
            event._status = 'CLOSED'
    return render_template('index.html', events = Event.query.all())
    
@app.route('/about')
def about():
    return render_template('about.html')
    
    
@app.route('/login/',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        zid = request.form['zid']
        password = request.form['password']

        if Eventsystem.check_digital(zid):
            if Eventsystem.validate_login(int(zid), password):
                login_user(Eventsystem.validate_login(int(zid), password))
                return redirect(url_for('index'))
            else:
                return render_template('login.html', val = True, message = 'Invalid zid or passsword')
        else:
            return render_template('login.html', val = True, message = 'Please enter zid as an integer')
    return render_template('login.html')


@app.route('/post/',methods = ['POST','GET'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        capacity = request.form['capacity']
        detail = request.form['detail']
        status = 'OPEN'

        if Eventsystem.check_data(start,end) and Eventsystem.check_digital(capacity):
            event = Event(title,detail,start,end,capacity,status,current_user.name)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('index'))
        elif Eventsystem.check_data(start,end) == False:
            return render_template('post.html', post = True, post_info = 'End date should less than start data!')
        elif Eventsystem.check_digital(capacity) == False:
            return render_template('post.html', post = True, post_info = 'Enter capacity as integer!')

    return render_template('post.html')

@app.route('/info/<eventId>',methods = ['POST','GET'])
@login_required
def info(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('info.html', event = event)

@app.route('/cancele/<eventId>',methods = ['POST','GET'])
@login_required
def cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    event.status = 'CANCELED'
    db.session.add(event)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/cance/',methods = ['POST','GET'])
@login_required
def cance():
    return render_template('canele.html',events = Event.query.all())

@app.route('/register/<eventId>',methods = ['POST','GET'])
@login_required
def register(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = User.query.filter_by(zid = current_user.zid).one()

    if user in event.events_all.all():
        flash('You alreay register this event!')
    else:
        event.users.append(user)
        # user.events.append(event)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/dashboard/')
@login_required
def dashboard():
    user = User.query.filter_by(zid = current_user.zid).one()
    return render_template('dashboard.html',regists = user.users_all.all())

@app.route('/user_curr/')
@login_required
def user_curr():
    user = User.query.filter_by(zid = current_user.zid).one()
    return render_template('dashboard.html',regists = user.users_all.all())

@app.route('/user_info/<eventId>',methods = ['POST','GET'])
@login_required
def user_info(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('userinfo.html', event = event)

@app.route('/user_past/',methods = ['POST','GET'])
@login_required
def user_past():
    user = User.query.filter_by(zid = current_user.zid).one()
    return render_template('userpast.html', regists = user.users_all.all())


@app.route('/user_cancele/<eventId>',methods = ['POST','GET'])
@login_required
def user_cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = User.query.filter_by(zid = current_user.zid).one()
    if user in event.users:
        event.users.remove(user)
        # user.events.remove(event)
        db.session.commit()
    else:
        return render_template('userinfo.html',val = True, message = 'deregister', event = event)

@app.route('/currpost/',methods = ['POST','GET'])
@login_required
def currpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    return render_template('currpost.html',events = events)

@app.route('/pastpost/',methods = ['POST','GET'])
@login_required
def pastpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    return render_template('pastpost.html',events = events)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



