from contextlib import closing
from flask import Flask, render_template, json, request, redirect, session, send_file
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'spooky action at a distance-Einstein'
CORS(app)
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1324'
app.config['MYSQL_DATABASE_DB'] = 'Project'
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
    return render_template('signin.html', signup= False)

@app.route('/userHome')
def userHome():
    global _name
    print()
    #print("session.get('user')",session.get('user'))
    if session.get('user'):
        return render_template('userHome.html', user=session['user'])
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
        
        
        if len(data) > 0:
            if (str(data[0][3]),_password):
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
                    conn.commit()
                    return render_template('signin.html',signup= True)
                else:
                    return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

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
	

if __name__ == "__main__":
    app.run(port=5000)
