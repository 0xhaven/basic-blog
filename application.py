from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect
from markdown import Markdown
from flask import Markup
from flask.ext.sqlalchemy import SQLAlchemy
import bleach
import os
import psycopg2


from models import *

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.app = application
db.init_app(application)
db.create_all()

safe_markdown = Markdown(safe_mode='escape')

### Routes
#Home page containing list of blog posts
#  GET returns index template, with list of all `blog_posts`
@application.route('/')
def index_page():
  try:
    blog_posts = BlogPost.query.order_by("timestamp")
  except:
    abort(500)
  return render_template('index.html', blog_posts=blog_posts)

#"Compose New Post" page/form endpoint
#  GET returns "Compose New Post" form
#
#  POST Client submits parameters:
#    `post_title` as raw string (to by html-escaped)
#    `post_body`  as Markdown string (to be marked up to HTML, escpaing raw HTML)
#  After post is saved, redirect to `/post/<post_id>`
@application.route('/compose', methods=['GET', 'POST'])
def compose_page():
  if request.method == 'GET':
    return render_template('compose.html')
  else:
    try:
      parsed_post_name = bleach.clean(request.form['post_title'])
      parsed_post_body = safe_markdown.convert(request.form['post_body'])
      blog_post = BlogPost(parsed_post_name, parsed_post_body)
      db.session.add(blog_post)
      db.session.commit()
    except:
      abort(400)
    return redirect("/post/{}".format(blog_post.post_id), code=303)
    
#Standalone Blog Post/Comments page/comment form endpoint
#  GET returns blog post along with comments and new comment form.
#  Returns 404 if post not found
#
#  POST saves new comment with parameter:
#    `comment_body` as Markdown string (to be marked up to HTML, escpaing raw HTML)
#  After comment is saved, redirect to relative link
#      `/post/<post_id>#<comment_id>` at head of comment.
@application.route('/post/<int:post_id>', methods=['GET', 'POST'])
def blogpost(post_id):
  if request.method == 'GET':
    try:
      blog_post = BlogPost.query.get(post_id)
      return render_template('post.html', blog_post=blog_post, comments=blog_post.comments)
    except:
      abort(404)
  elif request.method == 'POST':
    try:
      parsed_comment_body = safe_markdown.convert(request.form['comment_body'])
      comment = Comment(str(post_id), parsed_comment_body)
      db.session.add(comment)
      db.session.commit()
      comment_id = comment.comment_id
    except:
      abort(400)
    return redirect("/post/{}#{}".format(post_id,comment_id), code=303)
  else: #this should never be called
    abort(500)

#Endpoint to delete blog post
#  POST deletes blog post with paramter
#    `post_id` as primary key of post to be deleted
#  Returns 404 if post not found
#  After successful deletion, redirect to index
@application.route('/delete_post', methods=['POST'])
def delete_post():
  try:
    blog_post = BlogPost.query.get(request.form['post_id'])
    db.session.delete(blog_post)
    db.session.commit()
  except:
    abort(404)
  return redirect("/", code=303)

#Endpoint to delete comment
#  POST deletes comment with paramter:
#    `comment_id` as primary key of comment to be deleted
#  Returns 404 if comment not found
#  After successful deletion, redirect to start of comments (`/post/<post_id>#comments`)
@application.route('/delete_comment', methods=['POST'])
def delete_comment():
  try:
    comment = Comment.query.get(request.form['comment_id'])
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
  except:
    abort(404)
  return redirect("/post/{}#comments".format(post_id), code=303)

if __name__ == '__main__':
  application.run(debug=True)