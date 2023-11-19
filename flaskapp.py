from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_socketio import SocketIO, send, join_room, leave_room
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog12.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)
app.secret_key = 'my_secret_key'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db. String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    articles = db.relationship('Article', back_populates='user')
    sent_messages = db.relationship('Chat', foreign_keys='Chat.sender_id', backref='sent_messages_user')
    received_messages = db.relationship('Chat', foreign_keys='Chat.receiver_id', backref='received_messages_user')
    friends = db.relationship('Friendship', foreign_keys='Friendship.user_id', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User % {self.id}>"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='articles')

    def __repr__(self):
        return f"<Article % {self.id}>"

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    conversation_id = db.Column(db.String, nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages1')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages1')

    def __repr__(self):
        return f"<Chat % {self.id}>"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_mails')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_mails')

    def __repr__(self):
        return f"<Message % {self.id}>"

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_rel = db.relationship('User', foreign_keys=[user_id], overlaps='friends,user')
    friend_rel = db.relationship('User', foreign_keys=[friend_id], overlaps='friends,user')

    def __repr__(self):
        return f"<Friendship % {self.id}>"
