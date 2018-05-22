from event import User, Event,Seminar,Session,db
from abc import ABC, abstractmethod
from datetime import datetime
from ErrorMessage import ErrorMessage

class Eventsystem(ABC):

    def validate_login(zid, password):

        if zid is '' and password is '':
            raise ErrorMessage('zid and password', None)
        elif zid is'':
            raise ErrorMessage('zid',None)
        elif password is '':
            raise ErrorMessage('password', None)

        for user in User.query.all():
            if user.zid == zid and user.validate_password(password):
                return user
        raise ErrorMessage('zid and password', 'Please ensure the zid and password')
    
    def check_digital(num):

        if num.isdigit():
            return True
        else:
            raise ErrorMessage('number','Please ensure it is')

    def check_data(start, end):
        date_format = "%d-%m-%Y"
        start = datetime.strptime(start, date_format)
        start = start.strftime(date_format)

        end = datetime.strptime(end, date_format)
        end = end.strftime(date_format)

        if end > start:
            return True
        else:
            raise ErrorMessage('start and end date', 'Please ensure the start date is before the end date')
    
    
    def check_statu():
        now = datetime.now()
        now = now.strftime("%d-%m-%Y")

        for event in Event.query.all():
            if str(event.end) < now or event.capacity >= event.events_all.count():
                event.status = 'CLOSED'
                db.session.add(event)
                db.session.commit()
        for seminar in Seminar.query.all():
            if str(seminar.end) < now or seminar.capacity >= seminar.seminars_all.count():
                seminar.status = 'CLOSED'
                db.session.add(seminar)
                db.session.commit()
        for session in Session.query.all():
            if str(session.end) < now or session.capacity >= session.sessions_all.count():
                session.status = 'CLOSED'
                db.session.add(session)
                db.session.commit()

    def check_in(user, event):
        if user not in event.events_all.all():
            return True
        raise ErrorMessage(None,'You already registe this course')

    def check_userin(user, event):
        if user in event:
            return user
        raise ErrorMessage(None, 'You are not regist this event')

    def check_regist(event, seminar):
        if len(event) != 0 or len(seminar) != 0:
            return True
        raise ErrorMessage(None,'You have not regist any course or seminar!')

    def getSeminar(session):
        for seminar in Seminar.query.all():
            if session in seminar.sessions:
                return seminar
        
        return None

    def getUser(user, seminar):
        for session in seminar.seminar_all.all():       
            if user in session.users:
                return True
        return None
    
    def validate_login_guest(username, password):

        if username is '' and password is '':
            raise ErrorMessage('username and password', None)
        elif username is'':
            raise ErrorMessage('username',None)
        elif password is '':
            raise ErrorMessage('password', None)

        for user in User.query.all():
            if user.name == username and user.validate_password(password):
                return user
        raise ErrorMessage('username and password', 'Please ensure the user and password')

