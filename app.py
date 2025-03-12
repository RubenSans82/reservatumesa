from flask import Flask,render_template,request,redirect,url_for,session
import db
import bcrypt  # Add this import for password hashing
import json
from datetime import timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_user')
def login_page():
    return render_template('user/login_user.html')

@app.route('/user',methods=['POST'])
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
            datos = (username,)
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

@app.route('/booking/<int:restaurant_id>')
def booking(restaurant_id):
    connnection = db.get_connection()
    with connnection.cursor() as cursor:
        consulta = "SELECT * FROM reservation WHERE restaurant_id = %s"
        cursor.execute(consulta,(restaurant_id))
        bookings = cursor.fetchall()
        consulta = "SELECT * FROM restaurant WHERE restaurant_id = %s"
        cursor.execute(consulta,(restaurant_id))
        restaurant = cursor.fetchone()
    
    # Convertir timedelta a string
    for booking in bookings:
        if isinstance(booking['time'], timedelta):
            booking['time'] = str(booking['time'])
    
    connnection.close()
    return render_template('user/booking.html',bookings = bookings,restaurant = restaurant)

@app.route('/booking',methods=['POST'])
def add_booking():
    #obtener los datos del formulario
    restaurant_id = request.form['restaurant']
    client_id = request.form['user']
    date = request.form['date'] 
    time = request.form['time']
    diners = request.form['people']
    #creamos
    #TODO: Comprobar que el hueco de reserva sigue libre
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            #crear la consulta
            consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners) VALUES (%s,%s,%s,%s,%s)"
            datos = (restaurant_id,client_id,date,time,diners)
            cursor.execute(consulta,datos)
            conexion.commit()
            return redirect(url_for(''))
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:
        conexion.close()
        print("Conexión cerrada")

if __name__ == '__main__':
    app.run(debug=True,port=80)