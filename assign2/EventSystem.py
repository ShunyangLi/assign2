from event import db,User,Event
from abc import ABC, abstractmethod

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
    
