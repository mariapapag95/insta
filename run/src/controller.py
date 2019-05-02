from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from model import User, Posts
from werkzeug import secure_filename
import os

controller = Flask(__name__)
CONTROLLER_ROOT = os.path.join(os.path.dirname(__file__), 'static')
controller.config['UPLOAD_FOLDER'] = CONTROLLER_ROOT


@controller.route('/')
def homepage():
    return render_template('homepage.html')

@controller.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        u = User(username)
        if u.signup(username, password, confirm):  
            session["username"] = username  
            return redirect(url_for('dashboard'))
        else:
            error = 'That username is already taken. Choose another.'
            return render_template('signup.html', message=error)

@controller.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User(username)
        if u.login(password):
            session["username"] = username  
            return redirect(url_for('dashboard'))
        else:
            error = "Username or password inccorect. Try again."
            return render_template('login.html', message=error)

@controller.route('/<username>',methods=['GET','POST'])
def userpage(username):
    p = Posts()
    user_posts = p.user_page(username)
    if request.method == 'GET':
        return render_template('userpage.html', user_posts = user_posts, username = username) 

@controller.route('/dashboard', methods=['GET','POST'])
def dashboard():
    username = session["username"]
    p = Posts()
    allposts = p.allposts()
    if request.method == 'GET':
        return render_template('dashboard.html', allposts=allposts, username=username)
    elif request.method == 'POST':
        try:
            caption = request.form.get('caption')
            photo = request.files['photo']
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(controller.config['UPLOAD_FOLDER'], filename))
            u = User(username)
            if u.post(filename, caption):    
                return redirect(url_for('dashboard', filename=filename))
            else:
                message = "Your post was unsuccessful, please try again."
                return render_template('dashboard.html', allposts=allposts, message=message)  
        except KeyError:
            like = request.form.get('like')
            repost = request.form.get('repost')
            print(repost)
            follow = request.form.get('follow')
            u = User(username)
            if repost:
                if u.repost(repost):
                    print('it worked')
                    return redirect(url_for('dashboard'))
            if like:
                if u.like(like):
                    return redirect(url_for('dashboard'))

@controller.route('/logout',methods=['GET'])
def logout():
    try:
        if request.method == 'GET':
            session.pop('username') 
            return render_template('logout.html')
    except KeyError:
        return render_template('logout.html')

if __name__ == '__main__':
    print(CONTROLLER_ROOT)
    controller.secret_key = 'maria'
    controller.config['SESSION_TYPE'] = 'filesystem'
    controller.run(host='0.0.0.0', debug = True)