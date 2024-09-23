from flask import *
import pymysql



app=Flask(__name__)

connect=pymysql.connect(host='localhost',user='root',password='',database='Lake_view')
cursor = connect.cursor() 
app.secret_key="oreems"


@app.route('/')
def home():
    

    return render_template('index.html')


@app.route('/singup',methods=['POST','GET'])
def singup():
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password1=request.form['password1']
        password2=request.form['password2']

        
        if len(password1) <8:
            return render_template('singup.html',error='PASSWORD MUST BE MORE THAN 8 CHARACTERS')
        elif password1 != password2:
            return render_template('singup.html',error1="PASSWORD DON'T MATCH")
        else:
            sql='''INSERT INTO `users`(`username`, `password`, `email`, `phone`) VALUES (%s,%s,%s,%s)'''
            cursor.execute(sql,(username,password1,email,phone))
            connect.commit()
            
            return render_template('singup.html',success='SUCCESSFULLY SIGNED UP')
    else:
        return render_template('singup.html')
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username=request.form['username']
        password1=request.form['password1']

        login_query="SELECT * FROM users WHERE username= %s AND password= %s"
        cursor.execute(login_query,(username,password1))

        if cursor.rowcount == 0:
            return render_template('login.html',error='INVALID CREDENTIALS')
        else:
            session['key']=username 
            return redirect('/')
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logou():
    session.clear() # we are clearing the session
    return redirect('/login')

@app.route('/mpesa',methods=['POST','GET'])
def mpesa():
    #request the  amount and phone from single_item.html
    phone=request.form['phone']
    amount=request.form['amount']

    #import mpesa.py module
    import mpesa

    #call the stk_push function present in mpesa.py
    mpesa.stk_push(phone,amount)

    #return a message
    return '<h3>Please Complete Payment In Your Phone And We Will Deliver In Minutes</h3>'\
    '<a href='"/"' >Back To Home</a>'

@app.route('/Lake')
def Lake():
    return render_template('Lake.html')

@app.route('/Fish')
def Fish():

    return render_template('Fish.html')

@app.route('/Ponds')
def Ponds():
    
    return render_template('Ponds.html')

@app.route('/Hotels')
def Hotels():

    return render_template('Hotels.html')

if __name__=='__main__':
    app.run(debug=True)


















