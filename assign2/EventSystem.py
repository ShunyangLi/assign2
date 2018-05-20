from event import User, Event,Seminar,Session,db
from abc import ABC, abstractmethod
from datetime import datetime

class Eventsystem(ABC):

    def validate_login(zid, password):
        for user in User.query.all():
            if user.zid == zid and user.validate_password(password):
                return user
        return None
    
    def check_digital(num):
        if num.isdigit():
            return True
        else:
            return False

    def check_data(star, end):
        if end < star:
            return False
        else:
            return True
    
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

