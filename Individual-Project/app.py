from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import date



app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyDSnMiV1EB0HiYtbXCYrk0vlZRxQn0GI2c",
  "authDomain": "project-30a9d.firebaseapp.com",
  "projectId": "project-30a9d",
  "storageBucket": "project-30a9d.appspot.com",
  "messagingSenderId": "1067352441801",
  "appId": "1:1067352441801:web:9832cfa14491f6bcff1e18",
  "measurementId": "G-DVMVS3F4XP",
  "databaseURL":"https://project-30a9d-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def home():
    today = date.today()
    if db.child("Post").get().val() != None:
        post = db.child("Post").get().val()
        return render_template("index.html", posts = post, date = today)
    return render_template("index.html", date = today)

@app.route('/mypost', methods=['GET', 'POST'])
def mypost():
    if 'user' in login_session and login_session['user']!=None:
        UID = login_session['user']['localId']
        if db.child("Post").child(UID).get().val()!=None:
            myposts = db.child("Post").child(UID).get().val()
            print(myposts)
            return render_template("mypost.html", mypost = myposts)
        else:
            return redirect(url_for('post'))
    else:
        return redirect(url_for('signin'))

    return render_template("myposts.html")

@app.route('/post', methods=['GET', 'POST'])
def post():    
    error = ""
    if 'user' in login_session and login_session['user']!=None:
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['text']
            link = request.form['link']
            try:
                if title and text and link:
                    UID = login_session['user']['localId']
                    post = {"title" : title, "text" : text, "link" : link, "UID" : UID}
                    db.child("Post").child(UID).push(post)
                    return redirect(url_for('post'))
            except:
                error = "Authentication failed"
        return render_template("post.html")
    else:
        return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"full_name" : full_name, "username" : username, "bio" : bio}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    UID = login_session['user']['localId']
    db.child("Post").child(UID).remove()
    return redirect(url_for('mypost'))

#Code goes above here
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
if __name__ == '__main__':
    app.run(debug=True)