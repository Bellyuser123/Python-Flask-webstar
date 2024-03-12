from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy  # pip install flask_sqlalchemy
from werkzeug.utils import secure_filename  # pip install --upgrade werkzeug
from sqlalchemy.orm import DeclarativeBase  # pip install --upgrade sqlalchemy
from flask_mail import Mail, Message  # pip install flask_mail
import os
import math
import json

local_server = True
with open('config.json') as c:
    params = json.load(c)["params"]

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'gand-me-danda-le-teri-gand-me-danda-le'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_passwd'],
    MAIL_DEFAULT_SENDER=params['gmail_user']
)
mail = Mail(app)

if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Contacts(db.Model):
    serial = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=False)
    msg = db.Column(db.String, nullable=False)


class Signups(db.Model):
    serial = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=False)


class Projects(db.Model):
    serial = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, unique=False)
    slug = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    date = db.Column(db.String)


class Posts(db.Model):
    serial = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, unique=False)
    slug = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    date = db.Column(db.String)


@app.route("/")
def welcome():
    return render_template('welcome.html', params=params)


@app.route("/home")
def home():
    posts = Posts.query.filter_by().all()[0:params['num_index']]
    projects = Projects.query.filter_by().all()[0:params['num_index']]
    return render_template('index.html', params=params, projects=projects, posts=posts)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        table_type = request.form.get('table_type', 'projects')
        if request.method == 'POST':
            table_type = request.form.get('table_type', 'projects')
            if table_type == 'projects':
                data = Projects.query.all()
            elif table_type == 'posts':
                data = Posts.query.all()
            else:
                data = []
            return render_template('dashboard.html', params=params, data=data, table_type=table_type)
        data = Projects.query.all()
        return render_template('dashboard.html', params=params, data=data, table_type=table_type)
    elif request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('pass')
        if username == params['admin_user'] and password == params['admin_password']:
            session['user'] = username
            table_type = request.form.get('table_type', 'projects')
            if table_type == 'projects':
                data = Projects.query.all()
            elif table_type == 'posts':
                data = Posts.query.all()
            else:
                data = []
            return render_template('dashboard.html', params=params, data=data, table_type=table_type)
    return render_template('Login.html', params=params)


@app.route("/edit/<string:table_type>/<string:serial>", methods=['GET', 'POST'])
def editing_sec(serial, table_type):
    if 'user' in session and session['user'] == params['admin_user']:
        if table_type == 'projects':
            post = Projects.query.filter_by(serial=serial).first() if serial != 'new' else None
        elif table_type == 'posts':
            post = Posts.query.filter_by(serial=serial).first() if serial != 'new' else None
        else:
            post = None
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            image = request.form.get('image')
            date = request.form.get('date')
            content = request.form.get('content')
            content = content.replace('\n', '<br>')
            if not serial or serial == 'new':
                if table_type == 'projects':
                    post = Projects(serial=None, title=title, slug=slug, image=image, date=date, content=content)
                elif table_type == 'posts':
                    post = Posts(serial=None, title=title, slug=slug, image=image, date=date, content=content)
                db.session.add(post)
                db.session.commit()
                return redirect('/edit/' + table_type + '/' + serial)
            else:
                if table_type == 'projects':
                    post = Projects.query.filter_by(serial=serial).first()
                elif table_type == 'posts':
                    post = Posts.query.filter_by(serial=serial).first()

                if post:
                    post.title = title
                    post.slug = slug
                    post.image = image
                    post.date = date
                    post.content = content

                    db.session.commit()
                    return redirect('/edit/' + table_type + '/' + serial)
            return render_template('editing.html', params=params, serial=serial, table_type=table_type)
        if table_type == 'projects':
            post = Projects.query.filter_by(serial=serial).first()
        elif table_type == 'posts':
            post = Posts.query.filter_by(serial=serial).first()
        return render_template('editing.html', params=params, serial=serial, table_type=table_type, post=post)
    else:
        return render_template('404.html')


@app.route("/delete/<string:table_type>/<string:serial>")
def delete(serial, table_type):
    if 'user' in session and session['user'] == params['admin_user']:
        if table_type == 'projects':
            post = Projects.query.filter_by(serial=serial).first() if serial != 'new' else None
        elif table_type == 'posts':
            post = Posts.query.filter_by(serial=serial).first() if serial != 'new' else None
        else:
            post = None
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')
    else:
        return render_template('404.html')


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "uploaded successfully"
    else:
        return render_template('404.html')


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/signup", methods=['GET', 'POST'])
def sign_sec():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        entry = Signups(name=name, email=email)
        db.session.add(entry)
        db.session.commit()
        return "Signed up successfully"

    return render_template('signup.html', params=params)


@app.route("/about")
def abt_sec():
    return render_template('about.html', params=params)


@app.route("/proj/<string:proj_slug>", methods=['GET'])
def project_route(proj_slug):
    project = Projects.query.filter_by(slug=proj_slug).first()
    return render_template('project1.html', params=params, project=project)


@app.route("/projects")
def proj_sec():
    projects = Projects.query.filter_by().all()
    last = math.ceil(len(projects) / int(params['num_side_proj']))
    page = request.args.get('page', 1, type=int)
    page = int(page)
    offset = (page - 1) * int(params['num_side_proj'])
    projects = projects[offset:offset + int(params['num_side_proj'])]
    prev = page - 1 if page > 1 else '#'
    after = page + 1 if page < last else '#'
    return render_template('projects.html', params=params, projects=projects, prev=prev, after=after)


@app.route("/blog")
def blog_sec():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['num_side_post']))
    page = request.args.get('page', 1, type=int)
    page = int(page)
    offset = (page - 1) * int(params['num_side_post'])
    posts = posts[offset:offset + int(params['num_side_post'])]
    prev = page - 1 if page > 1 else '#'
    after = page + 1 if page < last else '#'
    return render_template('blog.html', params=params, posts=posts, prev=prev, after=after)


@app.route("/blog/<string:blog_slug>")
def blogs(blog_slug):
    post = Posts.query.filter_by(slug=blog_slug).first()
    return render_template('blog1.html', params=params, post=post)


@app.route("/contact", methods=['GET', 'POST'])
def cont_sec():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg_content = request.form.get('message')
        entry = Contacts(name=name, email=email, msg=msg_content)
        db.session.add(entry)
        db.session.commit()

        subject = 'New Message From Your Website'
        recipient_email = params['gmail_user']

        msg = Message(subject, recipients=[recipient_email])
        msg.body = f"Name: {name}\n\nEmail: {email}\n\nMessage Content: {msg_content}"

        mail.send_message('New Feedback Form Your Website',
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=str(msg)
                          )

    return render_template('contact.html', params=params)


app.run(debug=True)
