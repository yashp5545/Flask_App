from flask import Flask, render_template,request,session
import main as db
app = Flask(__name__)
obj = db.Bot()
from apscheduler.schedulers.background import BackgroundScheduler
from flask_session import Session


scheduler = BackgroundScheduler()
scheduler.start()
app.secret_key = 'secret_key'

@app.route('/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        number = request.form['number']
        statename = request.form['stateID']
        session['number'] = number
        session['statename'] = statename
        
        data = obj.voterdata(number, statename)
        print(data)
        if data:
            return render_template('image.html',items=data)
    return render_template('index.html')

@app.route('/img',methods=['GET','POST'])
def img():
    if request.method == 'POST':
        Captcha = request.form['Captcha']
        data = obj.captchadata(Captcha)
        
        return render_template('mobileotp.html')

@app.route('/mobileotp',methods=['GET','POST'])
def mobileotp():
    if request.method == 'POST':
        OTP = request.form['OTP']
        data = obj.getcsv(OTP)
        print(data,'yash')
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
