from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import db
import bcrypt  # Add this import for password hashing

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_user',methods=['POST'])
def login():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    #creamos la conexion
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            #creamos la consulta - solo buscamos por username
            consulta = "SELECT * FROM client WHERE username = %s"
            datos = (username,)
            cursor.execute(consulta,datos)
            usuario = cursor.fetchone()
            if usuario:
                # Verificamos la contraseña con bcrypt
                stored_password = usuario['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    #guardar datos en session
                    session['username'] = username
                    return redirect(url_for('user'))
                else:
                    return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
            else:
                return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:    
        conexion.close()
        print("Conexión cerrada") 
        
@app.route('/user')
def user():
    return render_template('user/home.html')