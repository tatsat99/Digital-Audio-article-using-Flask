from flask import Flask, request, render_template, redirect, url_for
from gtts import gTTS
import pyqrcode
from pydrive.auth import GoogleAuth
from pyqrcode import QRCode
import shutil
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
import pyqrcode
import os
from PIL import Image

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)
folder_id = 'your-drive-folder-id'
import string
import re

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'database-config' #username and password
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = folder



class User(UserMixin, db.Model):
    __tablename__ = 'editors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True)
    password = db.Column(db.Unicode)

class Article(db.Model):
    __tablename__ = 'info'
    author = db.Column(db.Unicode)
    doc = db.Column(db.Unicode,primary_key=True)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired() ])
    remember = BooleanField('remember me')


    

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if form.username.data == 'manager':
            return redirect(url_for('manager'))
        elif user:
            return redirect(url_for('convert',username=form.username.data))
        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)
	
	
@app.route('/manager', methods=["GET","POST"])
def manager():
    errors = ""
    if request.method == "POST":
            info = Article.query.all()
            return render_template("new.php", info=info)
    return '''
    <html>
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
 integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>

<body style="background:url('/static/images/homepage4.jpg') no-repeat center fixed; background-size:100%;">
<div style="background-color:#e60000;color:#ffffff;height:100px"></br><h1 class="display-5"><p class="text-center">Text to Speech</p></h1></div>
<div  class="container-fluid" style="height:75px">
</div>
</br>
<div class="container-fluid">
<div class="row">
<div class="col">
	</div>
	<div class ="col-7">
		<div class="card">
			<div class="card-body" style="background-color:#e60000;color:#ffffff; ">
			</div>
			<div class="card-body">
				<form class="form-group"  method="post">
					<input type ="submit" name="publications" class="btn btn-primary"  value="See publications">
				</form>
			</div>
		</div>
		</div>
		<div class="col">
		</div>
</div>
</div>

    '''


@app.route('/convert/<string:username>', methods=["GET", "POST"])
def convert(username):
    errors = ""
    if request.method == "POST":
        text = None
        try:
            text = str(request.form["text"])
        except:
            errors += "error"
        if text is not None:
            result = do_conversion(text,username)
            print(result)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], result)
            #return render_template("qrDisp.html", img=full_filename)
            return '''
                    <html>
                    <head>
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
                     integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                    </head>
                    <body style="background:url('/static/images/homepage4.jpg') no-repeat center fixed; background-size:100%;">
                    <div style="background-color:#e60000;color:#ffffff;height:100px"></br><h1 class="display-5"><p class="text-center">Text to Speech</p></h1></div>
                    <div  class="container-fluid" style="height:75px">
                    </div>
                    </br>
                    <div class="container-fluid">
                    <div class="row">
                    <div class="col">
                            </div>
                            <div class ="col-7">
                                    <div class="card">
                                            <div class="card-body" style="background-color:#e60000;color:#ffffff; ">
                                            <h5> Generated Audio </h5>
                                            </div>
                                            <div class="card-body">
                                                            <label><b>QR Code :</b></label>
                                                            <img src="/static/images/{result}">
                                                            <br><br>
                                        <p> <a href = "/convert/{username}"> Click here to convert again </a> </p>
                                            </div>
                                            </div>
                                    </div>
                                    <div class="col">
                                    </div>
                    </div>
                    </div>
            '''.format(username=username, result=result)
    return '''
    <html>
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
 integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>

<body style="background:url('/static/images/homepage4.jpg') no-repeat center fixed; background-size:100%;">
<div style="background-color:#e60000;color:#ffffff;height:100px"></br><h1 class="display-5"><p class="text-center">Text to Speech</p></h1></div>
<div  class="container-fluid" style="height:75px">
</div>
</br>
<div class="container-fluid">
<div class="row">
<div class="col">
	</div>
	<div class ="col-7">
		<div class="card">
			<div class="card-body" style="background-color:#e60000;color:#ffffff; ">
			<h5> Generate Audio </h5>
			</div>
			<div class="card-body">
				<form class="form-group"  method="post">

					<label><b>Text to be converted :</b></label>
					<div class="input-group">
						<div class="input-group-prepend">
						</div>
						<textarea name="text" class="form-control" aria-label="With textarea" rows="5" required></textarea>
					</div>
					</br>
					<input type ="submit" class="btn btn-primary" name="text_submit" value="Convert">
				</form>
			</div>
		</div>
		</div>
		<div class="col">
		</div>
</div>
</div>

    '''


def do_conversion(n1,username):
    TTS = gTTS(text=str(n1), lang='en-uk')
    
    n2 = n1[0:5]
    n2.rstrip()
    n2.replace(" ", "a")
    
    TTS.save(n2+".mp3")

    file1 = drive.CreateFile({
        "mimeType": "audio/mpeg",
        'parents': [{'id': folder_id}]
    })



    file1.SetContentFile(n2+".mp3")
    file1.Upload()  # Upload the file.
    print(file1['id'])
    print('title: %s, mimeType: %s' % (file1['title'], file1['mimeType'],))

    s = "https://drive.google.com/open?id=" + file1['id']

    url = pyqrcode.create(s, error='H')

    
    fileName = n2 + ".png"
    url.png(fileName, scale=8)
    shutil.move(fileName, r'\static\images')

    u = Article(author=username, doc=n2)
    db.session.add(u)
    db.session.commit()

    return fileName
if __name__ == '__main__':
    app.run()
