from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'blogpostsecretkeyforlogin!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/zeeshan/Desktop/flask-bloggapp/blogapp.db'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    posts = db.relationship('Blogpost', backref='poster')

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    author = db.Column(db.String(20))
    content = db.Column(db.Text)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)
@app.route('/edit/<int:post_id>')
def edit(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('edit.html', post=post)

@app.route('/add')
@login_required
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, author=author, content=content, date_posted=datetime.now(), poster=current_user)

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))
@app.route('/editpost', methods=['POST'])
def editpost():
    id= request.form['id']
    post = Blogpost.query.filter_by(id=id).one()
    post.title = request.form['title']
    post.author =  request.form['author']
    post.content = request.form['content']
    db.session.commit()

    return redirect(url_for('dashboard'))
@app.route('/deletepost', methods=['POST'])
def deletepost():
    id= request.form['id']
    post = Blogpost.query.filter_by(id=id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    posts = Blogpost.query.filter_by(poster_id=current_user.id).all()
    return render_template('dashboard.html', name=current_user.username,posts=posts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
