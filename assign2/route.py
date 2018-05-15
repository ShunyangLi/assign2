from event import User, Event,db
from flask import Flask, render_template, request, url_for, redirect
from flask_login import current_user, login_required, login_user, logout_user

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/about')
def about():
    return render_template('about.html')
    
    
@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        zid = request.form['zid']
        password = request.form['password']
        
    return render_template('login.html')       
    

if __name__ == '__main__':
    app.run(debug = True)
