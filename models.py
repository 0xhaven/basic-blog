from flask.ext.sqlalchemy import SQLAlchemy
from flask import Markup

db = SQLAlchemy()

class BlogPost(db.Model):
  post_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
  timestamp     = db.Column(db.DateTime, default=db.func.now())
  title         = db.Column(db.String)
  body          = db.Column(db.String)

  comments      = db.relationship('Comment', backref='blogpost', cascade="all,delete")

  @property
  def num_comments(self):
    return db.session.query(Comment).with_parent(self, "comments").count()
  @property
  def pretty_time(self):
      return self.timestamp.strftime("%B %d, %Y at %H:%M:%S")
  

  def __init__(self, 
               title = None,
               body = None
              ):
    self.title = title  
    self.body  = body

class Comment(db.Model):
  comment_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
  timestamp     = db.Column(db.DateTime, default=db.func.now())
  post_id       = db.Column(db.Integer, db.ForeignKey('blog_post.post_id'))
  body          = db.Column(db.String)

  @property
  def pretty_time(self):
      return self.timestamp.strftime("%B %d, %Y at %H:%M:%S")

  def __init__(self,
               post_id = None,
               body = None
              ):
    self.post_id = post_id
    self.body        = body
