from flask import Flask
from flask import render_template

application = Flask(__name__)

### Routes
@application.route('/')
def index_page():
  return render_template('index.html')

if __name__ == '__main__':
  application.run(debug=True)