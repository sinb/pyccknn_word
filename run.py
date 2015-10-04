#!/usr/bin/env python
# coding=utf-8
from HTMLParser import HTMLParser
import os
import random
import codecs
import locale
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.mysqldb import MySQL
#global variables
app = Flask(__name__)

#################
# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=False,
    SECRET_KEY='asdf3',
    MYSQL_HOST='localhost',
    MYSQL_USER='',
    MYSQL_PASSWORD='',
    MYSQL_DB='russian',
    MYSQL_CHARSET='utf8'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
#####db
mysql = MySQL()
mysql.init_app(app)
################
def connect_db():
    db = mysql.connection
    return db
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db    

# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'mysql_db'):
#         g.mysql_db.close()

################login, logout#############
@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()

    error = None
    if request.method == 'POST':
        cur = db.cursor()
        cur.execute(''' select nickname from user''')
        namelist = cur.fetchall()
        cur.close()
        namelist = [name[0] for name in namelist]
        if request.form['username'] not in namelist:
            error = u'输错了!'
        else:
            session['logged_in'] = True
            flash('登录成功')
            return redirect(url_for('main_page'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('main_page'))
###########################################################
@app.route("/about")
def about_page():
    return render_template('about.html')
############main function##################
@app.route("/mylist")
def mylist():
    return render_template('mylist.html')
@app.route("/recite")
def recite():
    return render_template('mylist.html')
@app.route("/lookup", methods=['POST'])
def lookup():
    word = request.form['word']
    db = get_db()
    cur = db.cursor()
    cur.execute('''select * from `russiandic` where word="%s"'''%word.encode('utf-8').translate(None,"',.`|!?@"))
    result = cur.fetchone()
    cur.close()
    if result != None:
        return render_template('lookup.html', word=result[1], meaning=result[2], variants=result[3]) 
    else:   
        return render_template('lookup.html', word=word, meaning=u'没有找到%s'%word)
###########################################
@app.route("/")
def main_page():
    db = get_db()
    cur = db.cursor()
    cur.execute('''select * from `russiandic` where id=%d'''%random.randint(1,477102))
    # print 'cur!!'
    # print cur
    [id, word, meaning, variants] = cur.fetchone()
    cur.close()
    return render_template('main_page.html',word=word,meaning=meaning,variants=variants)
@app.route("/2")
def template_test2():
    return render_template('main_page.html', my_string="eeee!", my_list=[0,1,2,3,4,5])
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,threaded=True)
