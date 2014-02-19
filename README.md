basic-blog
==========
A sample implementation of a blog intended to capture example usage of [Flask](http://flask.pocoo.org/) and [Bootstrap](http://getbootstrap.com/).  Take a look at the [live version on Heroku](http://jhaven-basic-blog.herokuapp.com/).

Setup
------
1. `git clone https://github.com/QuicksilverJohny/basic-blog.git`
2. `cd basic-blog`
3. `pip install -r requirements.txt`
4. Setup dabase (see below)
5. `python application.py` OR `foreman start`


###Option 1: Postgres DB###
Start a postgres server and add to your `~/.profile`:
```
  export DB_URL=postgres://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_DATABASE
```

###Option 2: SQLite DB###
Replace `import psycopg2` with `import pysqlite2` *(NOTE: this will not work on Heroku)* and instead set:
```
  export DB_URL=sqlite:///test.db
```
