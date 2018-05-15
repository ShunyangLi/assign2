from flask_login import UserMixin
from server import db


event_realation = db.Table('event_realation',
    db.Column('event_id', db.Integer, db.ForeignKey('events.event_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'))
)

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    zid = db.Column(db.Integer, unique = True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(80))
    
    events = db.relationship('Event', secondary = event_realation,
                                backref=db.backref('events_all', lazy='dynamic'))
                                    
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
        return self.user_id
    
    def validate_password(self, password):
        return self.password == password
    
    def __repr__(self):
        return '<User: %r>'%self.name
        
        

class Event(db.Model):
    
    __tablename__ = 'events'
    
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    details = db.Column(db.Text)
    start = db.Column(db.String(80))
    end = db.Column(db.String(80))
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(80))
    creater = db.Column(db.String(80))
    
    users = db.relationship('User',secondary=event_realation,
                            backref=db.backref('users_all', lazy='dynamic'))
    
    
    def __init__(self,title,details,start,end,capacity,status, creater):
        self.title = title
        self.details = details
        self.start = start
        self.end = end
        self.capacity = capacity
        self.status = status
        self.creater = creater

    def __repr__(self):
        return '<Event: %r>'%self.title

