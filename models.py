from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BlogPost(db.Model):
  #__tablename__ = 'blogpost'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  timestamp     = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
  title         = db.Column(db.String)
  body          = db.Column(db.String)

  #comments      = db.relationship('Comment', backref='blogpost', lazy='dynamic')

  def __init__(self, 
               title = None,
               body = None
              ):
    self.title = title  
    self.body  = body

class Comment(db.Model):
  #__tablename__ = 'comment'
  id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
  timestamp     = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
  #blogpost_id   = db.Column(db.Integer, db.ForeignKey('blogpost.id'))
  body          = db.Column(db.String)

  def __init__(self, 
               body = None
              ):
    self.body  = body
