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
                # Get restaurant data
                query = "SELECT * FROM restaurant WHERE username = %s"
                data = (session['username'],)
                cursor.execute(query, data)
                restaurant = cursor.fetchone()
                
                if restaurant:
                    # Get date from query params or use today
                    from datetime import datetime, date
                    selected_date = request.args.get('date', date.today().isoformat())
                    
                    # Get reservations for this restaurant on selected date
                    query = """
                        SELECT r.*, c.username as client_name 
                        FROM reservation r
                        JOIN client c ON r.client_id = c.client_id
                        WHERE r.restaurant_id = %s AND r.date = %s
                    """
                    cursor.execute(query, (restaurant['restaurant_id'], selected_date))
                    all_reservations = cursor.fetchall()
                    
                    print(f"Found {len(all_reservations)} reservations for date {selected_date}")
                    for res in all_reservations:
                        print(f"Reservation: {res}")
                    
                    # Define time slots - Adding 15:00 and 23:00 time slots
                    lunch_slots = ["13:00", "13:30", "14:00", "14:30", "15:00"]
                    dinner_slots = ["20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00"]
                    time_slots = lunch_slots + ["break"] + dinner_slots
                    
                    # Create a reservation matrix (time_slot -> seat_index -> reservation)
                    reservation_matrix = {}
                    
                    for time_slot in time_slots:
                        if time_slot != "break":
                            reservation_matrix[time_slot] = {}
                    
                    # Process reservations to fit into the matrix
                    # Only show confirmed or pending reservations, not rejected ones
                    for reservation in all_reservations:
                        # Get status with a default value if it doesn't exist
                        status = reservation.get('status', 'pending')
                        
                        if status != 'rejected':  # Skip rejected reservations
                            # Convert time to string format
                            if hasattr(reservation['time'], 'strftime'):
                                res_time = reservation['time'].strftime('%H:%M')
                            else:
                                # Handle potential different time formats
                                time_str = str(reservation['time'])
                                # Strip seconds if they exist
                                if len(time_str) > 5:  # e.g. "13:00:00"
                                    res_time = time_str[:5]
                                else:
                                    res_time = time_str
                            
                            print(f"Processing reservation at time: {res_time}")
                            
                            # Check if this time is in our defined slots
                            if res_time in reservation_matrix:
                                # Find first available seat index
                                start_seat = 0
                                found_spot = False
                                
                                while start_seat < restaurant['capacity'] and not found_spot:
                                    if start_seat not in reservation_matrix[res_time]:
                                        # Check if we have enough consecutive seats
                                        can_fit = True
                                        for i in range(reservation['diners']):
                                            if (start_seat + i) in reservation_matrix[res_time] or (start_seat + i) >= restaurant['capacity']:
                                                can_fit = False
                                                break
                                        
                                        if can_fit:
                                            # Reserve all needed seats
                                            reservation_matrix[res_time][start_seat] = reservation
                                            found_spot = True
                                            break
                                    
                                    start_seat += 1
                    
                    for time_slot in time_slots:
                        if time_slot != "break":
                            print(f"Time slot {time_slot}: {reservation_matrix.get(time_slot, {})}")
                    
                    return render_template('restaurant/home.html', 
                                          restaurant=restaurant,
                                          time_slots=time_slots,
                                          reservation_matrix=reservation_matrix,
                                          selected_date=selected_date)
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
        
@app.route('/restaurant/reservations/<date>')
def restaurant_reservations(date):
    if 'username' in session and session.get('user_type') == 'restaurant':
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                # Get restaurant data
                query = "SELECT * FROM restaurant WHERE username = %s"
                data = (session['username'],)
                cursor.execute(query, data)
                restaurant = cursor.fetchone()
                
                if restaurant:
                    # Get reservations for this restaurant on selected date with client info
                    query = """
                        SELECT r.*, c.username as client_name 
                        FROM reservation r
                        JOIN client c ON r.client_id = c.client_id
                        WHERE r.restaurant_id = %s AND r.date = %s
                        ORDER BY r.time
                    """
                    cursor.execute(query, (restaurant['restaurant_id'], date))
                    reservations = cursor.fetchall()
                    
                    # Convert timedelta to string for display
                    for reservation in reservations:
                        if isinstance(reservation['time'], timedelta):
                            reservation['time'] = str(reservation['time'])
                    
                    return render_template('restaurant/reservations.html', 
                                          restaurant=restaurant,
                                          reservations=reservations,
                                          selected_date=date)
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

@app.route('/restaurant/update_reservation_status', methods=['POST'])
def update_reservation_status():
    if 'username' in session and session.get('user_type') == 'restaurant':
        reservation_id = request.form.get('reservation_id')
        new_status = request.form.get('status')
        date = request.form.get('date')
        
        print(f"Updating reservation {reservation_id} to status {new_status}")
        
        connection = db.get_connection()
        try:
            with connection.cursor() as cursor:
                # First verify this reservation belongs to the logged in restaurant
                verify_query = """
                    SELECT r.*, rest.username
                    FROM reservation r
                    JOIN restaurant rest ON r.restaurant_id = rest.restaurant_id
                    WHERE r.reservation_id = %s
                """
                cursor.execute(verify_query, (reservation_id,))
                result = cursor.fetchone()
                
                print(f"Verification result: {result}")
                
                if result and result['username'] == session['username']:
                    # First check if status column exists
                    try:
                        # Try to get current status
                        check_query = "SELECT status FROM reservation WHERE reservation_id = %s"
                        cursor.execute(check_query, (reservation_id,))
                        current_status = cursor.fetchone()
                        print(f"Current status: {current_status}")
                        
                        # Update the reservation status
                        update_query = "UPDATE reservation SET status = %s WHERE reservation_id = %s"
                        cursor.execute(update_query, (new_status, reservation_id))
                        connection.commit()
                        print(f"Status updated successfully to {new_status}")
                    except Exception as column_error:
                        print(f"Error with status column: {column_error}")
                        # Status column might not exist, try to add it
                        try:
                            alter_query = "ALTER TABLE reservation ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"
                            cursor.execute(alter_query)
                            connection.commit()
                            print("Added status column to reservation table")
                            
                            # Now try the update again
                            update_query = "UPDATE reservation SET status = %s WHERE reservation_id = %s"
                            cursor.execute(update_query, (new_status, reservation_id))
                            connection.commit()
                            print(f"Status updated successfully to {new_status} after adding column")
                        except Exception as alter_error:
                            print(f"Error adding status column: {alter_error}")
                            return render_template("home.html", message="Error updating reservation status")
                    
                    # Return to the reservations page
                    return redirect(url_for('restaurant_reservations', date=date))
                else:
                    return render_template("home.html", message="No tienes permiso para modificar esta reserva")
        except Exception as e:
            print(f"Ocurrió un error al actualizar la reserva: {e}")
            return render_template("home.html", message=f"Error al actualizar la reserva: {e}")
        finally:
            connection.close()
            print("Conexión cerrada")
    else:
        return redirect(url_for('login_pageRest'))

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
            # First check if status column exists
            try:
                #crear la consulta con status
                consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners,status) VALUES (%s,%s,%s,%s,%s,'pending')"
                datos = (restaurant_id,client_id,date,time,diners)
                cursor.execute(consulta,datos)
                conexion.commit()
            except Exception as column_error:
                print(f"Error with status column: {column_error}")
                # Status column might not exist, try to add it
                try:
                    alter_query = "ALTER TABLE reservation ADD COLUMN status VARCHAR(20) DEFAULT 'pending'"
                    cursor.execute(alter_query)
                    conexion.commit()
                    print("Added status column to reservation table")
                    
                    # Now try the insert again without status (it will use default)
                    consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners) VALUES (%s,%s,%s,%s,%s)"
                    datos = (restaurant_id,client_id,date,time,diners)
                    cursor.execute(consulta,datos)
                    conexion.commit()
                except Exception as alter_error:
                    print(f"Error adding status column: {alter_error}")
                    # Try without status column as last resort
                    consulta = "INSERT INTO reservation (restaurant_id,client_id,date,time,diners) VALUES (%s,%s,%s,%s,%s)"
                    datos = (restaurant_id,client_id,date,time,diners)
                    cursor.execute(consulta,datos)
                    conexion.commit()
            
            return redirect(url_for('booking', restaurant_id=restaurant_id))
    except Exception as e:
        print(f"Ocurrió un error al conectar a la bbdd: {e}")
        return render_template("home.html", message=f"Error al crear la reserva: {e}")
    finally:
        conexion.close()
        print("Conexión cerrada")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,port=80)