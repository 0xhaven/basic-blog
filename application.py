from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect
from markdown import Markdown
from flask.ext.sqlalchemy import SQLAlchemy
import bleach
import os
import pyscopg2

from models import *

application = Flask(__name__)

#dev_url = 'sqlite:////' + os.path.dirname(os.path.realpath(__file__)) + 'dev.db'
#Set up database, connection to server specified by environment variable DATABASE_URL
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(application)
db.init_app(application)
db.create_all()

safe_markdown = Markdown(safe_mode='escape')

### Routes
@application.route('/')
def index_page():
  return render_template('index.html')

@application.route('/compose', methods=['GET', 'POST'])
def compose_page():
  if request.method == 'GET':
    return render_template('compose.html')
  else:
    #try:
    parsed_post_name = bleach.clean(request.form['post_body'])
    parsed_post_body = safe_markdown.convert(request.form['post_body'])
    blog_post = BlogPost(parsed_post_name, parsed_post_body)
    #except:
    #  abort(400)
    db.session.add(blog_post)
    db.session.commit()
    redirect("/post/{}".format(blog_post.id), code=303)

@application.route('/post/<int:post_id>')
def show_post(post_id):
  if request.method == 'GET':
    blog_post = BlogPost.query.filter_by(id=str(id)).first()
    return render_template('/campaign/show_campaign.html', blog_post=blog_post)
  else:
    abort(400)


if __name__ == '__main__':
  application.run(debug=True)