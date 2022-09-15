from flask import Flask , render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#database model
class Urls(db.Model):
    id_ = db.Column("id_",db.Integer, primary_key=True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String(3))#3 indicates that it wont have strings of length more than 3.

    def __init__(self,long,short): #constructor
        self.long = long
        self.short = short
#id is not passed into the constructor because id is created by sqlalchemy by itself
@app.before_first_request
def create_tables():
    db.create_all() #create all columns inside the data base

def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)#the result will be list
        rand_letters = "".join(rand_letters)#converting list into strings
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters

@app.route('/',methods=['POST','GET'])
def home():
    if request.method=="POST":
        url_recieved=request.form["nm"]
        #check if url already exist in db
        found_url = Urls.query.filter_by(long=url_recieved).first()
        if found_url:
            #return url if found
            return redirect(url_for("display_short_url", url=found_url.short))

        else:
            #create short url if not found
            short_url =shorten_url()
            print(short_url)
            new_url=Urls(url_recieved,short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    
    else:
         return render_template('url_page.html')

@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url= Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url does not Exist</h1>'

        
if __name__=='__main__':
    app.run(port=5000,debug=True)

