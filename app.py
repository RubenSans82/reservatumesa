from flask import Flask,render_template,request,redirect,url_for,session
import db
import bcrypt  # Add this import for password hashing
from config import Config  # Import Config class

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY  # Set the secret key from Config

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_user')
def login_page():
    return render_template('user/login_user.html')

@app.route('/logged_user',methods=['POST'])
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
            datos = (username)
            cursor.execute(consulta,datos)
            usuario = cursor.fetchone()
            if usuario:
                # Verificamos la contraseña con bcrypt
                stored_password = usuario['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    #guardar datos en session
                    session['username'] = username
                    return redirect(url_for('userhome'))
                else:
                    return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
            else:
                return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:    
        conexion.close()
        print("Conexión cerrada") 
        
@app.route('/register_user')
def register_page():
    return render_template('user/register_user.html')
        
@app.route('/registered_user',methods=['POST'])
def register():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    phone = request.form['phone']
    #creamos la conexion
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            # Verificar si el usuario ya existe
            consulta = "SELECT * FROM client WHERE username = %s"
            datos = (username)
            cursor.execute(consulta,datos)
            usuario = cursor.fetchone()
            if usuario:
                return render_template("user/register_user.html",mensaje="El usuario ya existe")
            else:
                # Hash the password
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                #crear la consulta
                consulta = "INSERT INTO client (username,password,phone) VALUES (%s,%s,%s)"
                datos = (username,hashed,phone)
                cursor.execute(consulta,datos)
                conexion.commit()
                return render_template("home.html",mensaje="Usuario registrado correctamente")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:
        conexion.close()
        print("Conexión cerrada")
        
        
@app.route('/user')
def user():
    return render_template('user/home.html')

@app.route('/userhome')
def userhome():
    if 'username' in session:
        # coger la lista de restaurantes y sus datos
        conexion = db.get_connection()
        try:
            with conexion.cursor() as cursor:
                consulta = "SELECT * FROM restaurant"
                cursor.execute(consulta)
                restaurantes = cursor.fetchall()
                return render_template('user/home.html',restaurantes=restaurantes)
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
        finally:
            conexion.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('home'))        
        
        
        
        

if __name__ == '__main__':
    app.run(debug=True,port=80)