from flask_login import UserMixin
from server import db


event_realation = db.Table('event_realation', db.Model.metadata,
    db.Column('events_id', db.Integer, db.ForeignKey('events.event_id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.user_id'))
)

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    zid = db.Column(db.Integer, unique = True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(80))
    
    users = db.relationship('Event', secondary = event_realation,
                                backref=db.backref('users_all', lazy='dynamic'))
                                    
    def __init__(self, name, zid, email, password, role):
        self.name = name
        self.zid = zid
        self.email = email
        self.password = password
        self.role = role
    
    @property
    def get_zid(self):
        return self.zid
    
    @property
    def is_authenticated(self):        
        return True
    
    @property
    def is_active(self):
        return True
        
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    
    def validate_password(self, password):
        return self.password == password
    
    def __repr__(self):
        return '<User: %r>'%self.name
        
        

class Event(db.Model):
    
    __tablename__ = 'events'
    
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    details = db.Column(db.Text)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(80))
    
    events = db.relationship('User',secondary=event_realation,
                            backref=db.backref('event_all', lazy='dynamic'))
    
    
    def __init__(self,title,details,start,end,capacity,status):
        self._title = title
        self._details = details
        self._start = start
        self._end = end
        self._capacity = capacity
        self._status = status

    def __repr__(self):
        return '<Event: %r>'%self._title

