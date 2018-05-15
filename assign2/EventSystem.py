from event import db,User,Event
from abc import ABC, abstractmethod

class Eventsystem(ABC):

    def validate_login(zid, password):
        for user in User.query.all():
            if user.zid == zid and user.validate_password(password):
                return user
        return None
