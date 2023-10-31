#Importar las dependencias necesarias para el funcianamiento del proyecto 
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import datetime


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./static/img"

#Configuracion para la base de datos(Nombre, puerto, usuario y contraseña)

app.config["SECRET_KEY"] = "clavesecreta"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "sapphireinventory"

mysql = MySQL(app)


#Rutas para ejecutar peticiójn HTTP, con los metodos que hacen dicha petición
@app.route("/", methods=["GET"])
def index():
    if "email" in session:
        return redirect(url_for("main"))
    else:
        return render_template("index.html")
    
    
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["pass"]
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s",(email,password))
    user = cur.fetchone()
    cur.close()
    
    if user:
        session["email"] = email
        session["id"] = user[0]  
        session["name"] = user[1]
        session["lastName"] = user[2]
        return redirect(url_for("main") )
    else:
        return render_template("index.html", message = "Credenciales incorrectas")
    

@app.route("/main")
def main():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s",[email])
        users = cur.fetchone()
        
        curUserQty = mysql.connection.cursor()
        curUserQty.execute("SELECT COUNT(id) AS total FROM users")
        userQty = curUserQty.fetchall()
        
        curProductQty = mysql.connection.cursor()
        curProductQty.execute("SELECT COUNT(id_producto) as total FROM productos")
        productQty = curProductQty.fetchall()
        
        cur.close()
        curUserQty.close()
        curProductQty.close()
        
        
        return render_template("main.html", users= users,userQty = userQty[0], productQty = productQty[0])
    else:
        return redirect(url_for("index"))
    
@app.route("/usersPerfil")
def usersPerfil():
    email = session["email"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s",[email])
    users = cur.fetchall()
    cur.close()
    return render_template("usersPerfil.html", users= users[0])

@app.route("/insertarImg/<id>", methods=["POST"])
def insertarImg(id):
    img = request.files["img"]

    tiempo = datetime.now()
    horaActual = tiempo.strftime("%Y%H%M%S")
    if img.filename!="":
        nuevoNombre=horaActual+"_"+img.filename
        img.save(os.path.join(app.config["UPLOAD_FOLDER"], nuevoNombre))
    else:
        return redirect(url_for("usersPerfil"))
  
    cur = mysql.connection.cursor()
    cur.execute("""
           UPDATE users 
           SET img = %s
           WHERE id = %s
               """,(nuevoNombre,id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for("usersPerfil"))


@app.route("/mostrarImg/<id>")
def mostrarImg(id):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"]), id)


@app.route("/products")
def products():
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s",[email])
        users = cur.fetchall()
        curProducts = mysql.connection.cursor()
        curProducts.execute("SELECT * FROM productos")
        products = curProducts.fetchall()
        cur.close()
        curProducts.close()

        print(products)

        return render_template("products.html", users= users[0], products = products)
    else:
        return redirect(url_for("index"))
    
    
@app.route("/addProduct", methods=["POST"])
def addProduct():
    
    marca = request.form["marca"]
    nombreProducto = request.form["nombreProducto"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO productos(marca_producto,nombre_producto,descripcion_producto,cantidad_producto) VALUES(%s, %s,%s,%s)",(marca,nombreProducto,descripcion,cantidad))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for("products"))


@app.route("/deleteProduct", methods=["POST"])
def deleteProduct():
    productId = request.form["productId"]
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id_producto = %s",(productId))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("products"))


@app.route("/updateProduct/<productId>")
def updateProduct(productId):
    if "email" in session:
        email = session["email"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s",[email])
        users = cur.fetchall()
        
        curProducts = mysql.connection.cursor()
        curProducts.execute("SELECT * FROM productos WHERE id_producto = %s",(productId))
        products = curProducts.fetchall()

        print(products)

        return render_template("updateProduct.html", users= users[0], products = products[0])
    else:
        return redirect(url_for("index"))
    

@app.route("/updateProduct/<productId>", methods=["POST","GET"])
def updateProductId(productId):
    updateMarca = request.form["updateMarca"]
    updateNombreProducto = request.form["updateNombreProducto"]
    updateDescripcion = request.form["updateDescripcion"]
    updateCantidad = request.form["updateCantidad"]
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE productos SET marca_producto = %s, nombre_producto = %s, descripcion_producto = %s, cantidad_producto = %s WHERE id_producto = %s", (updateMarca,updateNombreProducto,updateDescripcion,updateCantidad,productId))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for("products"))









"""@app.route("/img/<imagen>")
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join("static/img"),imagen)
"""

@app.route("/logOut")
def logOut():
    session.clear()
    return redirect(url_for("index"))


#ejecutar la aplicación en un servidor local para pruebas, en este caso puerto 5000
if __name__ == "__main__":
    app.run(debug = True)