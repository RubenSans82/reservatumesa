from flask import Flask,render_template,request,redirect,url_for,session
import db
import bcrypt  # Add this import for password hashing

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Add this line to enable sessions

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login_user')
def login_page():
    return render_template('user/login_user.html')

@app.route('/login_restaurant')
def login_pageRest():
    return render_template('restaurant/login_restaurant.html')

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
                    session['user_type'] = 'client'
                    return redirect(url_for('user'))
                else:
                    return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
            else:
                return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
        return render_template("home.html",mensaje="Error de conexión a la base de datos")
    finally:    
        conexion.close()
        print("Conexión cerrada") 
        
@app.route('/restaurant',methods=['POST'])
def loginRest():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    #creamos la conexion
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            #creamos la consulta - solo buscamos por username
            consulta = "SELECT * FROM restaurant WHERE username = %s"
            datos = (username,)
            cursor.execute(consulta,datos)
            usuario = cursor.fetchone()
            if usuario:
                # Verificamos la contraseña con bcrypt
                stored_password = usuario['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    #guardar datos en session
                    session['username'] = username
                    session['user_type'] = 'restaurant'
                    return redirect(url_for('restaurant'))
                else:
                    return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
            else:
                return render_template("home.html",mensaje="Usuario o contraseña incorrecta")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
        return render_template("home.html",mensaje="Error de conexión a la base de datos")
    finally:    
        conexion.close()
        print("Conexión cerrada") 
                
@app.route('/register_user')
def register_page():
    return render_template('user/register_user.html')

@app.route('/register_restaurant')
def register_pageRest():
    return render_template('restaurant/register_restaurant.html')
        
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
        
@app.route('/registered_restaurant',methods=['POST'])
def registerRest():
    #obtener los datos del formulario
    username = request.form['username'] 
    password = request.form['password']
    restaurant_name = request.form['name']  # Changed from 'restaurant_name' to 'name'
    phone = request.form['phone']   
    address = request.form['address']
    website = request.form['website']
    capacity = request.form['capacity']
    description = request.form['description']
    #creamos la conexion
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            # Verificar si el usuario ya existe
            consulta = "SELECT * FROM restaurant WHERE username = %s"
            datos = (username)
            cursor.execute(consulta,datos)
            usuario = cursor.fetchone()
            if usuario:
                return render_template("restaurant/register_restaurant.html",mensaje="El usuario ya existe")
            else:
                # Hash the password
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                #crear la consulta
                consulta = "INSERT INTO restaurant (username, password, restaurant_name, phone, address, website, capacity, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                datos = (username, hashed, restaurant_name, phone, address, website, capacity, description)
                cursor.execute(consulta,datos)
                conexion.commit()
                return render_template("home.html",mensaje="Restaurante registrado correctamente")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:
        conexion.close()
        print("Conexión cerrada")
                
@app.route('/user')
def user():
    return render_template('user/home.html')
@app.route('/restaurant')
def restaurant():
    return render_template('restaurant/home.html')


if __name__ == '__main__':
    app.run(debug=True,port=80)