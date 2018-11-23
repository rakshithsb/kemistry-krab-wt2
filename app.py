from contextlib import closing
from flask import Flask, render_template, json, request, redirect, session, send_file, jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
import smtplib
import sched, time

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'spooky action at a distance-Einstein'
CORS(app)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'FlaskBlogApp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


_name = ""
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignin():
    if request.args.get('signup'):
        sgn = True
    else:
        sgn = False
    return render_template('signin.html', signup= sgn)

@app.route('/userHome')
def userHome():
    global _name
    print()
    #print("session.get('user')",session.get('user'))
    if session.get('user'):
        return render_template('home.html', user=session['user'])
    else:
        return  redirect("/")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
               
        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        #print("Data",check_password_hash(str(data[0][3])))
        print("_password",_password)
        print(data[0])
        if len(data) > 0:
            if (str(data[0][3])==_password):
                session['user'] = data[0][1]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')          

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    #_hashed_password = generate_password_hash(_password)
                    cursor.callproc('sp_createUser',(_name,_email,_password))
                    data = cursor.fetchall()

                if len(data) is 0:
                    return redirect("/showSignIn?signup=true")
                else:
                    return render_template('error.html',error = str(data[0]))
        else:
            return render_template('error.html',error = 'Enter the required fields')

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route('/instruction')
def instruction():
	return render_template('instruction.html')

g_intro_count = 0
file_names= ['1.gif','2.gif','3.gif']

@app.route('/intro_gif',methods=['GET'])
def intro_gif():	
	global g_intro_count
	global file_names
	filename = file_names[g_intro_count % 3]
	g_intro_count += 1
	return '/static/images/'+filename

@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html', user = session['user'])



@app.route('/quiz_info', methods=['GET'])
def quiz():
    if request.args.get('question_count'):
        question_count = int(request.args.get('question_count'))
    else:
        question_count = None
      
    questions = [{"q":"Easy Question 1",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2}, {"q":"Easy Question 2",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2},
        {"q":"Easy Question 3",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2}]
        
    if question_count is not None:
        if question_count > 1:
            questions = [{"q":"Tough Question 1",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2}, {"q":"Tough Question 2",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2},
            {"q":"Tough Question 3",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2}]
        
        elif question_count > 0:
            questions = [{"q":"Medium Question 1",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2}, {"q":"MEdium Question 2",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2},
            {"q":"Medium Question 3",1:"Wrong",2:"Right",3:"Incorrect",4:"False",'r':2}]
            
   
      
    return jsonify(questions)

# s = sched.scheduler(time.time, time.sleep)
# def send(): 
# 	server = smtplib.SMTP('smtp.gmail.com', 587)
# 	server.starttls()
# 	server.login("rakshith.s.budihal@gmail.com", "Your Password")
 
# 	msg = "Test1!"
# 	server.sendmail("rakshith.s.budihal@gmail.com", "rakshith.s.budihal@gmail.com", msg)
# 	server.quit()

# def print_some_times():
# 	print ("time1",time.time())
# 	s.enter(5, 1, send, ())
# 	s.enter(8, 1, send, ())
# 	s.run()
# 	print ("time2",time.time())
	
# print_some_times()

if __name__ == "__main__":
    app.run(port=5000)
