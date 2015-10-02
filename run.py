#!/usr/bin/env python
# coding=utf-8
from HTMLParser import HTMLParser
import os
import random
import codecs
import locale
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
#global variables
mysql = MySQL()
app = Flask(__name__)
hparser = HTMLParser()
#################
# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flaskr.db'),
     DEBUG=True,
    SECRET_KEY='asdf3',
    USERNAME='',
    MYSQL_DATABASE_HOST='localhost',
    MYSQL_DATABASE_USER='root',
    MYSQL_DATABASE_PASSWORD='',
    MYSQL_DATABASE_DB='russian',
    MYSQL_CHARSET='utf-8'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
## mysql cursor
mysql.init_app(app)
conn = mysql.connect()
cur = mysql.connect().cursor()
## db properity
cur.execute('''select max(id) from russian_chn''')
MAX_ITEM_ID = cur.fetchone()
MAX_ITEM_ID = MAX_ITEM_ID[0]
cur.execute('''select min(id) from russian_chn''')
MIN_ITEM_ID = cur.fetchone()
MIN_ITEM_ID = MIN_ITEM_ID[0]
################login, logout#############
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
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
    # word = hparser.unescape(word)
    cur.execute('''select * from `russian_chn` where word="%s"'''%word)
    result = cur.fetchone()
    if result != None:
        return render_template('lookup.html', word=result[1], meaning=result[3], variants=result[2]) 
    else:   
        return render_template('lookup.html', word=word, meaning=u'没有找到%s'%word)
###########################################
@app.route("/")
def main_page():
    cur.execute('''select * from `russian_chn` where id=%d'''%random.randint(MIN_ITEM_ID,MAX_ITEM_ID))
    [id, word, variants, meaning] = cur.fetchone()
    return render_template('main_page.html',word=word,meaning=meaning,variants=variants)
@app.route("/2")
def template_test2():
    return render_template('main_page.html', my_string="eeee!", my_list=[0,1,2,3,4,5])
    
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    except (KeyboardInterrupt, SystemExit):
        conn.close()