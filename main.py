from flask import Flask, render_template, request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]



app = Flask(__name__)
# For mail when someone sends you a message|
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)


app.secret_key = 'super-secret-key'

# Connecting to local server
local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

   

# Home page
@app.route("/")
def home():
     return render_template('index.html', params=params)

# Inner page
@app.route("/inner-page")
def inner_page():
     return render_template('inner-page.html', params=params)

# Contact Me page
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
     if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name=name,subject=subject,  message = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = subject + "\n" + message
                          )
     return render_template('contact.html', params=params)
     

# Portfolio Details page
@app.route("/portfolio-details")
def portfolio_details():
     return render_template('portfolio-details.html', params=params)


# Portfolio Details page
@app.route("/project-details")
def project_details():
     return render_template('project_details.html', params=params)


if __name__ =="__main__":
    app.run(debug=True)

