from flask.ext.sqlalchemy import SQLAlchemy
from flask import Markup

db = SQLAlchemy()

#Model for a blog post:
#All `title` and `body` strings are guaranteed to already be HTML escaped
class BlogPost(db.Model):
  post_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
  timestamp     = db.Column(db.DateTime, default=db.func.now())
  title         = db.Column(db.String) #HTML-escaped (using bleach) string
  body          = db.Column(db.String) #Markdown formated string (also escapes html)
  
  #relationship to child comments. They will be cascade deleted upon post deletion
  comments      = db.relationship('Comment', backref='blogpost', cascade="all,delete")

  #`blog_post.num_comments` counts the number of child comments this post has.
  @property
  def num_comments(self):
    return db.session.query(Comment).with_parent(self, "comments").count()
  #`blog_post.pretty_time` is a pretty-printed timestamp: "MMM DD, YYYY at HH:MM:SS"
  @property
  def pretty_time(self):
      return self.timestamp.strftime("%B %d, %Y at %H:%M:%S")
  

  def __init__(self, 
               title = None,
               body = None
              ):
    self.title = title  
    self.body  = body

#Model for a comment
#`body` string is guaranteed to already be HTML escaped
class Comment(db.Model):
  comment_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
  timestamp     = db.Column(db.DateTime, default=db.func.now())
  post_id       = db.Column(db.Integer, db.ForeignKey('blog_post.post_id'))
  body          = db.Column(db.String) #Markdown formated string (also escapes html)

  #`comment.pretty_time` is a pretty-printed timestamp: "MMM DD, YYYY at HH:MM:SS"
  @property
  def pretty_time(self):
      return self.timestamp.strftime("%B %d, %Y at %H:%M:%S")

  def __init__(self,
               post_id = None,
               body = None
              ):
    self.post_id = post_id
    self.body        = body
