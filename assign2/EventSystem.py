import re
from event import User, Event,Seminar,Session,db
# from abc import ABC, abstractmethod
from datetime import datetime
from ErrorMessage import ErrorMessage

"""
if we donnot want to use abstractmethod,
then can try to use staticmethod or staticmethod
"""


class Eventsystem():

    @staticmethod
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

    @staticmethod
    def remove_all_user(event):
        if len(event.users) != 0:
            for user in event.users:
                event.users.remove(user)
            db.session.commit()

    @staticmethod
    def validate_capacity(capacity):
        if int(capacity) > 0:
            return True
        else:
            raise ErrorMessage(None,'Capacity should greater than zero')
    
    @staticmethod
    def validate_period(start, end, period):
        start = datetime.strptime(start, "%d-%m-%Y")
        end = datetime.strptime(end,"%d-%m-%Y")
        diff = end - start

        if diff.days >= int(period):
            if int(period) >= 0:
                return True
            else:
                raise ErrorMessage(None,'Early period should greater or equal zero')
        else:
            raise ErrorMessage(None, 'Early period should between start and end')
        
        

    @staticmethod
    def cal_fee(start, user, event):
        start = datetime.strptime(start, "%d-%m-%Y")
        now = datetime.now()
        diff = now - start

        if user.role == 'guest':
            if diff.days <= event.early_period:
                user.fee = event.fee / 2
            else:
                user.fee = event.fee

    @staticmethod
    def validate_cancele(end):
        end = datetime.strptime(end, "%d-%m-%Y")
        now = datetime.now()
        
        if now - end >= 1:
            return True
        else:
            raise ErrorMessage(None, 'No more than 24 hours, sorry, can not cancele this event')

    @staticmethod
    def check_unique(username):
        user = User.query.filter_by(name = username).first()
        if user == None:
            return True
        else:
            raise ErrorMessage(None, 'This is username have been used, change another one')

    @staticmethod
    def validateEmail(email):
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return 1
        raise ErrorMessage(None,'Please enter email type as a username')

    @staticmethod
    def check_digital(num):
        if num.isdigit():
            return True
    
    @staticmethod
    def get_user(current_user):
        if current_user.role != 'guest':
            user = User.query.filter_by(zid = current_user.zid).one()
        else:
            user = User.query.filter_by(name = current_user.name).one()
        return user

    @staticmethod
    def check_data(start, end):
        date_format = "%d-%m-%Y"
        start = datetime.strptime(start, date_format)

        end = datetime.strptime(end, date_format)

        if end > start:
            return True
        else:
            raise ErrorMessage('start and end date', 'Please ensure the start date is before the end date')
    
    @staticmethod
    def check_start(start):
        now = datetime.now()
        start = datetime.strptime(start, "%d-%m-%Y")

        if start >= now:
            return True
        else:
            raise ErrorMessage(None, 'Please enter start date before today')

    @staticmethod
    def check_statu():
        now = datetime.now()
        
        for event in Event.query.all():
            end = datetime.strptime(event.end, "%d-%m-%Y")
            if end < now:
                event.status = 'CLOSED'
                db.session.add(event)
                db.session.commit()
        for seminar in Seminar.query.all():
            end = datetime.strptime(seminar.end, "%d-%m-%Y")
            if end < now:
                seminar.status = 'CLOSED'
                db.session.add(seminar)
                db.session.commit()
        for session in Session.query.all():
            end = datetime.strptime(session.end, "%d-%m-%Y")
            if end < now:
                session.status = 'CLOSED'
                db.session.add(session)
                db.session.commit()

    @staticmethod
    def validateRegistCourse(event):
            
        if event.capacity >= len(event.users) + 1:
            return True
        else:
            raise ErrorMessage(None, 'This course is full')
    
    @staticmethod
    def validateRegistSession(session):
        if session.capacity >= len(session.users) + 1:
            print(len(session.users))
            return True
        else:
            raise ErrorMessage(None, 'This session is full')
    
    @staticmethod
    def validateRegistSeminar(seminar):
        if seminar.capacity >= len(seminar.users) + 1:
            return True
        else:
            raise ErrorMessage(None, 'This seminar is full')
    
    @staticmethod
    def validate_Seminar_regist(user, seminar):
        if user not in seminar:
            return True
        else:
            raise ErrorMessage(None, 'You already regist this seminar')

    @staticmethod
    def Validate_Session_regist(user, session):
        if user not in session:
            return True
        else:
            raise ErrorMessage(None, 'You already regist this session')

    @staticmethod
    def check_in(user, event):
        if user not in event.events_all.all():
            return True
        raise ErrorMessage(None,'You already registe this course')

    @staticmethod
    def check_userin(user, event):
        if user in event:
            return user
        raise ErrorMessage(None, 'You are not regist this event')

    @staticmethod
    def check_regist(event, seminar):
        if len(event) != 0 or len(seminar) != 0:
            return True
        raise ErrorMessage(None,'You have not regist any course or seminar!')

    @staticmethod
    def getSeminar(session):
        for seminar in Seminar.query.all():
            if session in seminar.sessions:
                return seminar
        return None

    @staticmethod
    def getUser(user, seminar):
        for session in seminar.seminar_all.all():       
            if user in session.users:
                return True
        return None
    
    @staticmethod
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

