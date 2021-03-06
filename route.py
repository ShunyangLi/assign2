from server import app
from functools import wraps
from EventSystem import Eventsystem, ErrorMessage
from event import User, Event,Seminar,Session,db
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_login import current_user, login_required, login_user, logout_user

def admin_required(f):
    """This is used to check the admin status of the user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'trainer':
            return redirect(url_for('page_not_found'))
        return f(*args, **kwargs)
    return decorated_function


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
            guest = Eventsystem.make_register(username,password)
            Eventsystem.add_register(guest)
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
@admin_required
def post():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        fee = request.form['fee']
        capacity = request.form['capacity']
        detail = request.form['detail']
        status = 'OPEN'
        early_period = request.form['early_period']

        try:
            Eventsystem.check_start(start)
            Eventsystem.check_data(start, end)
            Eventsystem.valida_seminar_capa(capacity)
            Eventsystem.validate_period(start,end,early_period)
            event = Eventsystem.make_course(title,detail,start,end,capacity,status,current_user.name,fee,early_period)
            Eventsystem.add_course(event)
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
@admin_required
def cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    Eventsystem.remove_all_user(event)
    event.status = 'CANCELED'
    Eventsystem.add_course(event)
    return redirect(url_for('index'))

@app.route('/cance/',methods = ['POST','GET'])
@login_required
@admin_required
def cance():
    return render_template('canele.html',events = Event.query.all(), seminars = Seminar.query.all())


@app.route('/registercomfirme/<eventId>/',methods = ['POST','GET'])
@login_required
def registercomfirme(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = Eventsystem.get_user(current_user)

    if event:
        Eventsystem.cal_fee(event.start,user,event)
        return render_template('comfirm.html', event = event, user=user)
    else:
        user.fee = 0
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
        return render_template('usercurr.html',events = events, seminars = seminars)
    except ErrorMessage as error:
        return render_template('usercurr.html', dash = True, message = error.msg)

@app.route('/user_past/',methods = ['POST','GET'])
@login_required
def user_past():
    user = Eventsystem.get_user(current_user)
    events = user.event_users_all.all()
    seminars = user.seminar_users_all.all()

    try:
        Eventsystem.check_regist(events, seminars)
        return render_template('userpast.html',events = events, seminars = seminars)
    except ErrorMessage as error:
        return render_template('userpast.html', dash = True, message = error.msg)


@app.route('/user_cancele/<eventId>',methods = ['POST','GET'])
@login_required
def user_cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = Eventsystem.get_user(current_user)

    try:
        Eventsystem.validate_cancele(event.end)
        user = Eventsystem.check_userin(user, event.users)
        event.users.remove(user)
        db.session.commit()
        return render_template('info.html', event = event, cance = True, message = 'Cancele success')
    except ErrorMessage as error:
        return render_template('info.html', event = event, canerror = True, message = error.msg)

@app.route('/currpost/',methods = ['POST','GET'])
@login_required
@admin_required
def currpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    seminars = Seminar.query.filter_by(creater = current_user.name).all()
    return render_template('currpost.html',events = events, seminars = seminars)


@app.route('/pastpost/',methods = ['POST','GET'])
@login_required
@admin_required
def pastpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    seminars = Seminar.query.filter_by(creater = current_user.name).all()
    return render_template('pastpost.html',events = events, seminars = seminars)


@app.route('/info/<eventId>/participant/',methods = ['POST','GET'])
@login_required
@admin_required
def participant(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('participant.html',user = event.events_all.all())

@app.route('/postSeminar/',methods = ['POST','GET'])
@login_required
@admin_required
def postSeminar():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        capacity = request.form['capacity']
        detail = request.form['detail']
        status = 'OPEN'

        try:
            Eventsystem.check_start(start)
            Eventsystem.check_data(start, end)
            Eventsystem.valida_seminar_capa(capacity)
            seminar = Eventsystem.make_seminar(title,detail,start,end,capacity,status,current_user.name)
            Eventsystem.add_seminar(seminar)
            return redirect(url_for('index'))
        except ErrorMessage as error:
            return render_template('postseminar.html', val_post = True, post_info = error.msg)

    return render_template('postseminar.html')


@app.route('/Seminarcancele/<SeminarId>',methods = ['POST','GET'])
@login_required
@admin_required
def Seminarcancele(SeminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(SeminarId)).one()
    Eventsystem.remove_all_user(seminar)
    Eventsystem.cancele_all_session(seminar)
    seminar.status = 'CANCELED'
    Eventsystem.add_seminar(seminar)
    return redirect(url_for('index'))


@app.route('/seminarinfo/<SeminarId>/addsession',methods = ['POST','GET'])
@login_required
@admin_required
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
        early_period = request.form['early_period']
        status = 'OPEN'

        try:
            Eventsystem.check_start(start)
            Eventsystem.check_data(start, end)
            Eventsystem.validate_capacity(seminar, capacity)
            Eventsystem.validate_period(start,end,early_period)
            Eventsystem.chcek_speaker(speaker)
            session = Session(title,detail,start,end,capacity,status,current_user.name, speaker, fee,early_period)
            Eventsystem.add_session(session)
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
    sesminar = Eventsystem.getSeminar(session)
    user = Eventsystem.get_user(current_user)

    if session:
        Eventsystem.cal_fee(session.start,user,session)
        if Eventsystem.guest_speaker(sesminar, user):
            user.fee = 0
        return render_template('registsessioncomfirm.html', session = session, user = user)
    else:
        user.fee = 0
        return redirect(url_for('page_not_found'))


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
        Eventsystem.speakerof_seesion(user,session)
        session.users.append(user)
        db.session.commit()
        if Eventsystem.validate_Seminar_regist(user, seminar.users):
            seminar.users.append(user)
            db.session.commit()
        return render_template('sessioninfo.html', sessions = session, succ = True, message = 'Success regist')
    except ErrorMessage as error:
        return render_template('sessioninfo.html', regist = True, message = error.msg, sessions = session)

@app.route('/cancelesession/<sessionId>',methods = ['POST','GET'])
@login_required
def cancelesession(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    user = Eventsystem.get_user(current_user)
    seminar = Eventsystem.getSeminar(session)

    try:
        Eventsystem.validate_cancele(session.end)
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
@admin_required
def Sessioncancele(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    seminar = Eventsystem.getSeminar(session)
    Eventsystem.remove_session_user(session,seminar)
    Eventsystem.remove_all_user(session)
    session.status = 'CANCELED'
    Eventsystem.add_session(session)
    return redirect(url_for('index'))

@app.route('/sessioninfo/<sessionId>/participant_session/',methods = ['POST','GET'])
@login_required
@admin_required
def participant_session(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    return render_template('participant_session.html',user = session.sessions_all.all())

@app.route('/404')
def page_not_found():
    return render_template('404.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


