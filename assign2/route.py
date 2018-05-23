from server import app
from EventSystem import Eventsystem, ErrorMessage
from event import User, Event,Seminar,Session,db
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def index():
    Eventsystem.check_statu()
    return render_template('index.html', events = Event.query.all(), seminars = Seminar.query.all())
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/registerguest/', methods = ['POST','GET'])
def registerguest():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            Eventsystem.validateEmail(username)
            guest = User(username,None ,username,password,'guest')
            db.session.add(guest)
            db.session.commit()
            return render_template('successful.html', user = guest)
        except ErrorMessage as error:
            return render_template('register.html', re = True, message = error.msg)
    
    return render_template('register.html')

@app.route('/login/',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        zid = request.form['zid']
        password = request.form['password']

        if Eventsystem.check_digital(zid):
            try:
                user = Eventsystem.validate_login(int(zid), password)
                login_user(user)
                return redirect(url_for('index'))
            except ErrorMessage as error:
                return render_template('login.html', val = True, message = error.msg)
        else:
            try:
                user = Eventsystem.validate_login_guest(zid, password)
                login_user(user)
                return redirect(url_for('index'))
            except ErrorMessage as error:
                return render_template('login.html',val = True, message = error.msg)
    return render_template('login.html')


@app.route('/post/',methods = ['POST','GET'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        fee = request.form['fee']
        capacity = request.form['capacity']
        detail = request.form['detail']
        status = 'OPEN'
        try:
            Eventsystem.check_start(start)
            Eventsystem.check_data(start, end)
            event = Event(title,detail,start,end,capacity,status,current_user.name,fee)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('index'))
        except ErrorMessage as error:
            return render_template('post.html', val_post = True, post_info = error.msg)
    return render_template('post.html')

@app.route('/info/<eventId>',methods = ['POST','GET'])
@login_required
def info(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('info.html', event = event)


@app.route('/seminarinfo/<seminarId>',methods = ['POST','GET'])
@login_required
def seminarinfo(seminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(seminarId)).one()
    sessions = seminar.seminar_all.all()
    return render_template('seminarinfo.html', seminar = seminar, sessions = sessions)


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
    return render_template('canele.html',events = Event.query.all(), seminars = Seminar.query.all())


@app.route('/registercomfirme/<eventId>/',methods = ['POST','GET'])
@login_required
def registercomfirme(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = Eventsystem.get_user(current_user)

    if event:
        return render_template('comfirm.html', event = event, user=user)
    else:
        return 'Not find'

@app.route('/register/<eventId>',methods = ['POST','GET'])
@login_required
def register(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = Eventsystem.get_user(current_user)

    try:
        Eventsystem.validateRegistCourse(event)
        Eventsystem.check_in(user,event)
        event.users.append(user)
        db.session.commit()
        return render_template('info.html', event = event)
    except ErrorMessage as error:
        return render_template('info.html', event = event, event_in = True, message = error.msg)

@app.route('/dashboard/')
@login_required
def dashboard():
    user = Eventsystem.get_user(current_user)
    events = user.event_users_all.all()
    seminars = user.seminar_users_all.all()

    try:
        Eventsystem.check_regist(events, seminars)
        return render_template('dashboard.html',events = events, seminars = seminars)
    except ErrorMessage as error:
        return render_template('dashboard.html', dash = True, message = error.msg)

@app.route('/user_curr/')
@login_required
def user_curr():
    user = Eventsystem.get_user(current_user)
    events = user.event_users_all.all()
    seminars = user.seminar_users_all.all()

    try:
        Eventsystem.check_regist(events, seminars)
        return render_template('dashboard.html',events = events, seminars = seminars)
    except ErrorMessage as error:
        return render_template('dashboard.html', dash = True, message = error.msg)

@app.route('/user_past/',methods = ['POST','GET'])
@login_required
def user_past():
    user = Eventsystem.get_user(current_user)
    events = user.event_users_all.all()
    seminars = user.seminar_users_all.all()
    return render_template('userpast.html', events=events,seminars=seminars)


@app.route('/user_cancele/<eventId>',methods = ['POST','GET'])
@login_required
def user_cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = Eventsystem.get_user(current_user)

    try:
        user = Eventsystem.check_userin(user, event.users)
        event.users.remove(user)
        db.session.commit()
        return render_template('info.html', event = event, cance = True, message = 'Cancele success')
    except ErrorMessage as error:
        return render_template('info.html', event = event, canerror = True, message = error.msg)

@app.route('/currpost/',methods = ['POST','GET'])
@login_required
def currpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    seminars = Seminar.query.filter_by(creater = current_user.name).all()
    return render_template('currpost.html',events = events, seminars = seminars)


@app.route('/pastpost/',methods = ['POST','GET'])
@login_required
def pastpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    seminars = Seminar.query.filter_by(creater = current_user.name).all()
    return render_template('pastpost.html',events = events, seminars = seminars)


@app.route('/info/<eventId>/participant/',methods = ['POST','GET'])
@login_required
def participant(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('participant.html',user = event.events_all.all())

@app.route('/postSeminar/',methods = ['POST','GET'])
@login_required
def postSeminar():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        capacity = request.form['capacity']
        detail = request.form['detail']
        status = 'OPEN'

        try:
            Eventsystem.check_data(start, end)
            seminar = Seminar(title,detail,start,end,capacity,status,current_user.name)
            db.session.add(seminar)
            db.session.commit()
            return redirect(url_for('index'))
        except ErrorMessage as error:
            return render_template('postseminar.html', val_post = True, post_info = error.msg)

    return render_template('postseminar.html')


@app.route('/Seminarcancele/<SeminarId>',methods = ['POST','GET'])
@login_required
def Seminarcancele(SeminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(SeminarId)).one()
    seminar.status = 'CANCELED'
    db.session.add(seminar)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/seminarinfo/<SeminarId>/addsession',methods = ['POST','GET'])
@login_required
def addsession(SeminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(SeminarId)).one()
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        fee = request.form['fee']
        capacity = request.form['capacity']
        detail = request.form['detail']
        speaker = request.form['speaker']
        status = 'OPEN'

        try:
            Eventsystem.check_data(start, end)
            session = Session(title,detail,start,end,capacity,status,current_user.name, speaker, fee)
            db.session.add(session)
            db.session.commit()
            seminar.sessions.append(session)
            db.session.commit()
            return redirect(url_for('index'))
        except ErrorMessage as error:
            return render_template('postsession.html', val_post = True, post_info = error.msg)
    return render_template('postsession.html')

@app.route('/sessioninfo/<sessionId>',methods = ['POST','GET'])
@login_required
def sessioninfo(sessionId):
    sessions= Session.query.filter_by(session_id = sessionId).one()
    return render_template('sessioninfo.html', sessions = sessions)

@app.route('/registsessioncomfirm/<sessionId>',methods = ['POST','GET'])
@login_required
def registsessioncomfirm(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    user = Eventsystem.get_user(current_user)

    if session:
        return render_template('registsessioncomfirm.html', session = session, user = user)
    else:
        return 'Not find'


@app.route('/registsession/<sessionId>',methods = ['POST','GET'])
@login_required
def registsession(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    user = Eventsystem.get_user(current_user)
    seminar = Eventsystem.getSeminar(session)

    try:
        Eventsystem.validateRegistSession(session)
        Eventsystem.validateRegistSeminar(seminar)
        Eventsystem.Validate_Session_regist(user, session.sessions_all.all())
        Eventsystem.validate_Seminar_regist(user, seminar.users)
        session.users.append(user)
        db.session.commit()
        seminar.users.append(user)
        db.session.commit()
        return render_template('sessioninfo.html', sessions = session, succ = True, message = 'Success regist')
    except ErrorMessage as error:
        return render_template('sessioninfo.html', regist = True, message = error.msg, sessions = session)

    """
    if user in session.sessions_all.all():
        flash('You alreay register this event!')
    else:
        session.users.append(user)
        db.session.commit()
    if user not in seminar.users:
        seminar.users.append(user)
        db.session.commit()
    return redirect(url_for('index'))
    """

@app.route('/cancelesession/<sessionId>',methods = ['POST','GET'])
@login_required
def cancelesession(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    user = Eventsystem.get_user(current_user)
    seminar = Eventsystem.getSeminar(session)

    try:
        user = Eventsystem.check_userin(user, session.users)
        session.users.remove(user)
        db.session.commit()
    except ErrorMessage as error:
        return render_template('sessioninfo.html',sessions = session,not_in=True, message = error.msg)

    if Eventsystem.getUser(user, seminar):
        pass
    else:
        seminar.users.remove(user)
        db.session.commit()

    return render_template('sessioninfo.html',sessions = session)


@app.route('/Sessioncancele/<sessionId>',methods = ['POST','GET'])
@login_required
def Sessioncancele(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    session.status = 'CANCELED'
    db.session.add(session)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/sessioninfo/<sessionId>/participant_session/',methods = ['POST','GET'])
@login_required
def participant_session(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    return render_template('participant_session.html',user = session.sessions_all.all())


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


