from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect
from markdown import Markdown


application = Flask(__name__)

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
    print request
    print request.form
    for i in request.form:
      print i
    print request.form['post_body']
    #try:
    return safe_markdown.convert(request.form['post_body'])
    #except:
    #  abort(400)

if __name__ == '__main__':
  application.run(debug=True)