from flask import Flask,render_template,request,redirect,url_for,session
import db
import bcrypt  # Add this import for password hashing
from config import Config  # Import Config class
import json
from datetime import timedelta

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY  # Set the secret key from Config

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_user')
def login_page():
    return render_template('user/login_user.html')

@app.route('/login_restaurant')
def login_pageRest():
    return render_template('restaurant/login_restaurant.html')

@app.route('/logged_user',methods=['POST'])
def login():
    #obtener los data del formulario
    username = request.form['username'] 
    password = request.form['password']
    #creamos la connection
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            #creamos la query - solo buscamos por username
            query = "SELECT * FROM client WHERE username = %s"
            data = (username)
            cursor.execute(query,data)
            user = cursor.fetchone()
            if user:
                # Verificamos la contraseña con bcrypt
                stored_password = user['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    #guardar data en session
                    session['username'] = username
                    session['client_id'] = user['client_id']
                    return redirect(url_for('userhome'))
                else:
                    return render_template("user/login_user.html",message="usurario o contraseña incorrecta")
            else:
                return render_template("user/login_user.html",message="usurario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
        return render_template("home.html",mensaje="Error de conexión a la base de datos")
    finally:    
        connection.close()
        print("Conexión cerrada") 
        
@app.route('/restaurant',methods=['POST'])
def loginRest():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    #creamos la connection
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            #creamos la query - solo buscamos por username
            query = "SELECT * FROM restaurant WHERE username = %s"
            data = (username,)
            cursor.execute(query, data)
            user = cursor.fetchone()
            if user:
                # Verificamos la contraseña con bcrypt
                stored_password = user['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    #guardar datos en session
                    session['username'] = username
                    session['user_type'] = 'restaurant'
                    return redirect(url_for('restaurant'))
                else:
                    return render_template("restaurant/login_restaurant.html", message="Usuario o contraseña incorrecta")
            else:
                return render_template("restaurant/login_restaurant.html", message="Usuario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
        return render_template("home.html", message="Error de conexión a la base de datos")
    finally:    
        connection.close()
        print("Conexión cerrada")
                
@app.route('/register_user')
def register_page():
    return render_template('user/register_user.html')

@app.route('/register_restaurant')
def register_pageRest():
    return render_template('restaurant/register_restaurant.html')
        
@app.route('/registered_user',methods=['POST'])
def register():
    #obtener los data del formulario
    username = request.form['username'] 
    password = request.form['password']
    phone = request.form['phone']
    #creamos la connection
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Verificar si el user ya existe
            query = "SELECT * FROM client WHERE username = %s"
            data = (username)
            cursor.execute(query,data)
            user = cursor.fetchone()
            if user:
                return render_template("user/register_user.html",message="El usurario ya existe")
            else:
                # Hash the password
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                #crear la query
                query = "INSERT INTO client (username,password,phone) VALUES (%s,%s,%s)"
                data = (username,hashed,phone)
                cursor.execute(query,data)
                connection.commit()
                return render_template("user/login_user.html",message="usurario registrado correctamente")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:
        connection.close()
        print("Conexión cerrada")
        
@app.route('/registered_restaurant',methods=['POST'])
def registerRest():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    restaurant_name = request.form['name']
    phone = request.form['phone']   
    address = request.form['address']
    website = request.form['website']
    capacity = request.form['capacity']
    description = request.form['description']
    #creamos la conexion
    connection = db.get_connection()
    try:
        with connection.cursor() as cursor:
            # Verificar si el usuario ya existe
            query = "SELECT * FROM restaurant WHERE username = %s"
            data = (username,)
            cursor.execute(query, data)
            user = cursor.fetchone()
            if user:
                return render_template("restaurant/register_restaurant.html", message="El usuario ya existe")
            else:
                # Hash the password
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                #crear la consulta
                query = "INSERT INTO restaurant (username, password, restaurant_name, phone, address, website, capacity, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (username, hashed, restaurant_name, phone, address, website, capacity, description)
                cursor.execute(query, data)
                connection.commit()
                return render_template("home.html", message="Restaurante registrado correctamente")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
        return render_template("home.html", message="Error al registrar el restaurante")
    finally:
        connection.close()
        print("Conexión cerrada")
                
@app.route('/user')
def user():
    return render_template('user/home.html')

@app.route('/restaurant')
def restaurant():
    if 'username' in session and session.get('user_type') == 'restaurant':
        # Get the logged in restaurant information
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM restaurant WHERE username = %s"
                data = (session['username'],)
                cursor.execute(query, data)
                restaurant = cursor.fetchone()
                if restaurant:
                    return render_template('restaurant/home.html', restaurant=restaurant)
                else:
                    # Something went wrong with the session data
                    session.pop('username', None)
                    session.pop('user_type', None)
                    return redirect(url_for('home'))
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
            return render_template("home.html", message="Error de conexión a la base de datos")
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('login_pageRest'))

@app.route('/logout_restaurant')
def logout_restaurant():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('home'))

@app.route('/userhome')
def userhome():
    if 'username' in session:
        # coger la lista de restaurantes y sus data
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM restaurant ORDER BY restaurant_name ASC"
                cursor.execute(query)
                restaurants = cursor.fetchall()
                return render_template('user/home.html',restaurants=restaurants)
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('home'))    
    
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_details(restaurant_id):
    if 'username' in session:
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM restaurant WHERE restaurant_id = %s"
                data = (restaurant_id,)  # Add comma to make this a tuple
                cursor.execute(query,data)
                restaurant = cursor.fetchone()
                return render_template('user/restaurant.html', restaurant=restaurant)
        except Exception as e:
            print("Ocurrió un error al conectar a la bbdd: ", e)
        finally:
            connection.close()
            print("Conexión cerrada")    
    else:
        return redirect(url_for('home'))
        
        
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
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:
        conexion.close()
        print("Conexión cerrada")
        return redirect(url_for('userhome'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/my_reservations')
def my_reservations():
    print("DEBUG: Entrando a my_reservations")  # Para debug
    # Verificar si el usuario está logueado
    if 'username' not in session or 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Obtener todas las reservas del usuario con detalles del restaurante
            query = """
            SELECT r.*, rest.restaurant_name, rest.address, rest.image 
            FROM reservation r 
            JOIN restaurant rest ON r.restaurant_id = rest.restaurant_id 
            WHERE r.client_id = %s
            ORDER BY r.date, r.time
            """
            cursor.execute(query, (client_id,))
            reservations = cursor.fetchall()
            
            # Asegúrate de que la siguiente línea de código esté presente:
            print("Finalizando my_reservations")
            return render_template('user/my_reservations.html', 
                                  reservations=reservations, 
                                  username=session['username'])
    except Exception as e:
        print("Error al obtener reservas:", e)
        return render_template('user/my_reservations.html', 
                              message="Error al cargar tus reservas", 
                              reservations=[])
    finally:
        connection.close()

@app.route('/update_reservation/<int:reservation_id>', methods=['POST'])
def update_reservation(reservation_id):
    # Verificar si el usuario está logueado
    if 'username' not in session or 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    diners = request.form.get('diners')
    date = request.form.get('date')
    time = request.form.get('time')
    
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar que la reserva pertenece al usuario
            check_query = "SELECT * FROM reservation WHERE reservation_id = %s AND client_id = %s"
            cursor.execute(check_query, (reservation_id, client_id))
            reservation = cursor.fetchone()
            
            if not reservation:
                return redirect(url_for('my_reservations'))
            
            # Actualizar la reserva
            update_query = """
            UPDATE reservation 
            SET diners = %s, date = %s, time = %s
            WHERE reservation_id = %s AND client_id = %s
            """
            cursor.execute(update_query, (diners, date, time, reservation_id, client_id))
            connection.commit()
            
            return redirect(url_for('my_reservations'))
    except Exception as e:
        print("Error al actualizar reserva:", e)
        connection.rollback()
        return redirect(url_for('my_reservations'))
    finally:
        connection.close()

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    # Verificar si el usuario está logueado
    if 'username' not in session or 'client_id' not in session:
        return redirect(url_for('login_page'))
    
    client_id = session['client_id']
    connection = db.get_connection()
    
    try:
        with connection.cursor() as cursor:
            # Verificar que la reserva pertenece al usuario
            check_query = "SELECT * FROM reservation WHERE reservation_id = %s AND client_id = %s"
            cursor.execute(check_query, (reservation_id, client_id))
            reservation = cursor.fetchone()
            
            if not reservation:
                return redirect(url_for('my_reservations'))
            
            # Eliminar la reserva
            delete_query = "DELETE FROM reservation WHERE reservation_id = %s AND client_id = %s"
            cursor.execute(delete_query, (reservation_id, client_id))
            connection.commit()
            
            return redirect(url_for('my_reservations'))
    except Exception as e:
        print("Error al cancelar reserva:", e)
        connection.rollback()
        return redirect(url_for('my_reservations'))
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=80)