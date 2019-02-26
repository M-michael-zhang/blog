import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@123.207.233.171:3306/Huang"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)



class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Integer, unique=True)
    title = db.Column(db.String, unique=True)
    author = db.Column(db.String(16),unique=True)
    content = db.Column(db.String, unique=True)
    filename = db.Column(db.String, unique=True)
    time = db.Column(db.DateTime)
    # 给Role类创建一个uses属性，关联users表。
    # backref是反向的给User类创建一个role属性，关联roles表。这是flask特殊的属性。
    # users = db.relationship('User', backref="role")

    # 相当于__str__方法。
    def __repr__(self):
        return "article: %s %s %s %s %s %s " % (self.id, self.subject,self.title, self.author, self.content, self.time, self.filename)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self, id, subject, title, author, content, time, filename):
        self.id = id
        self.subject = subject
        self.title = title
        self.author = author
        self.content = content
        self.time = time
        self.filename = filename


class Subject(db.Model):
    __tablename__ = "subject"
    sid = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.Integer, unique=True)
    generalSubject = db.Column(db.Integer,unique=True)
    def __repr__(self):
        return "article: %s %s %s" % (self.sid, self.sname, self.generalSubject)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self, sid, sname, generalSubject):
        self.sid = sid
        self.sname = sname
        self.generalSubject = generalSubject



class GeneralSubject(db.Model):
    __tablename__ = "generalSubject"
    gid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return "article: %s %s " % (self.gid, self.name)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self, gid, name):
        self.gid = gid
        self.name = name


class Comment(db.Model):
    __tablename__ = "comment"
    cid = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, unique=True)
    reader = db.Column(db.String, unique=True)
    content = db.Column(db.String, unique=True)
    time = db.Column(db.DateTime)
    def __repr__(self):
        return "article: %s %s  %s %s %s  " % (self.cid, self.aid, self.reader, self.content, self.time)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self, cid, aid, reader, content, time):
        self.cid = cid
        self.aid = aid
        self.reader = reader
        self.content = content
        self.time = time


class InnerComment(db.Model):
    __tablename__ = "innerComment"
    icid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, unique=True)
    reader = db.Column(db.String, unique=True)
    content = db.Column(db.String, unique=True)
    time = db.Column(db.DateTime)
    def __repr__(self):
        return "article: %s %s  %s %s %s  " % (self.icid, self.caid, self.reader, self.content, self.time)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self, icid, cid, reader, content, time):
        self.icid = icid
        self.cid = cid
        self.reader = reader
        self.content = content
        self.time = time

class Liked(db.Model):
    __tablename__ = "liked"
    likedid = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, unique=True)
    reader = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return "article: %s %s  %s " % (self.likedid,  self.aid, self.reader)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self,likedid, aid, reader):
        self.likedid = likedid
        self.aid = aid
        self.reader = reader

class Disliked(db.Model):
    __tablename__ = "disliked"
    dlikedid = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, unique=True)
    reader = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return "article: %s %s  %s " % (self.dlikedid,  self.aid, self.reader)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __init__(self,dlikedid, aid, reader):
        self.dlikedid = dlikedid
        self.aid = aid
        self.reader = reader