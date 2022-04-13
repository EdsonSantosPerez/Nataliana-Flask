#Importamos los módulos a usar de flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
#Importamos los módulos de seguridad para las funciones hash
from werkzeug.security import generate_password_hash, check_password_hash

#Importamos el método login_required de flask_security
from flask_security import login_required
#Importamos los métodos login_user, logout_user flask_security.utils
#########################################################################################
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
##########################################################################################
#Importamos el modelo del usuario
from . models import Productos
#Importamos el objeto de la BD y userDataStore desde __init__
from . import db



#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
productos = Blueprint('productos', __name__)

@productos.route('/registerProductos')
@login_required #Parar proteger la ruta, con inicio de sesion
def registerProductos():
    return render_template('/registerProductos.html')

@productos.route('/registerProductos', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def registerProductos_post():
    tipo = request.form.get('tipo')
    nameVG = request.form.get('nameVG')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    imagen = request.form.get('imagen')
    color = request.form.get('color')
    materiales = request.form.get('materiales')
    status = True

    #Consultamos si existe un usuario ya registrado con el email.
    producto = Productos.query.filter_by(name=nameVG).first()

    if producto: #Si se encontró un producto
        flash('El producto ya existe, se modifico')
        return redirect(url_for('productos.consultarProductos'))

    #Si no existe, creamos un nuevo producto con sus datos.
    new_product = Productos(tipo=tipo ,name=nameVG, color=color, precio=precio, cantidad=cantidad, imagen=imagen, materiales=materiales, status=status)    
    
    db.session.add(new_product)
    #Añadimos el nuevo producto a la base de datos.
    db.session.commit()

    return redirect(url_for('productos.consultarProductos'))

@productos.route('/consultarProductos')
@login_required #Parar proteger la ruta, con inicio de sesion
def consultarProductos():
   #todosProductos = db.session.query(Productos).all()
    todosProductos = Productos.query.filter_by(status=1).all()
    return render_template('/consultarProductos.html', todosProductos= todosProductos)

@productos.route('/ventaRapida')
def ventaRapida():
   #todosProductos = db.session.query(Productos).all()
    todosProductos = Productos.query.filter_by(status=1).all()
    return render_template('/ventaRapida.html', todosProductos= todosProductos)

@productos.route('/carrito')
def carrito():
   #todosProductos = db.session.query(Productos).all()
    todosProductos = Productos.query.filter_by(status=1).all()
    return render_template('/carrito.html', todosProductos= todosProductos)

@productos.route('/venderProductos')
def venderProductos():
   #todosProductos = db.session.query(Productos).all()
    todosProductos = Productos.query.filter_by(status=1).all()
    return render_template('/venderProductos.html', todosProductos= todosProductos)

@productos.route('/productosClient') #Parar proteger la ruta, con inicio de sesion
def productosClient():
   #todosProductos = db.session.query(Productos).all()
    todosProductos = Productos.query.filter_by(status=1).all()
    return render_template('/productosClient.html', todosProductos= todosProductos)


#Definimos la ruta para eliminar productos
@productos.route('/eliminarProducto/<int:id>')
@login_required #Parar proteger la ruta, con inicio de sesion
def eliminarProducto(id):
    producto = db.session.query(Productos).filter(Productos.id == id).first()
    producto.status=False
    db.session.commit()
    return redirect(url_for('productos.consultarProductos'))

#Definimos la ruta para modificar productos
@productos.route('/modificarProducto/<id>')
@login_required #Parar proteger la ruta, con inicio de sesion
def modificarProducto(id):
    print("MUESTRO PAGE")
    producto = db.session.query(Productos).filter(Productos.id == id).first()  
    return render_template('/modificarProductos.html', producto= producto)

@productos.route('/productosClient', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def carritoProductos_post():
    tipo = request.form.get('tipo')
    nameVG = request.form.get('nameVG')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    imagen = request.form.get('imagen')
    color = request.form.get('color')
    status = True

    #Consultamos si existe un usuario ya registrado con el email.
    producto = Productos.query.filter_by(name=nameVG).first()

    if producto: #Si se encontró un producto
        flash('El producto ya existe, se modifico')
        return redirect(url_for('productos.consultarProductos'))

    producto = db.session.query(Productos).filter(Productos.id == id).first() 
    #Añadimos el nuevo producto a la base de datos.
    db.session.commit()

    return redirect(url_for('productos.productosClient'))

@productos.route('/buscarProducto', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def buscarProducto():
   #todosProductos = db.session.query(Productos).all()
    tipo = str(request.form.get('searchtipo'))
    todosProductos = Productos.query.filter_by(tipo = tipo).filter_by(status=1).all()
    
    return render_template('/consultarProductos.html', todosProductos= todosProductos)

@productos.route('/modificarProductos/<id>', methods=['POST'], )
@login_required #Parar proteger la ruta, con inicio de sesion
def modificarProductos_post(id):
    print("HIZO CLICK")
    producto = Productos.query.get(id)
    print(id)
    print(producto.id)
    print(producto.tipo)
    print(producto.name)
    print(producto.precio)
    print(producto.cantidad)
    print(producto.imagen)
    print(producto.color)
    print(producto.materiales)
    print(request.form.get('tipo'))
    print(request.form.get('nameVG'))
    print(request.form.get('precio'))
    print(request.form.get('cantidad'))
    print(request.form.get('imagen'))
    print(request.form.get('color'))
    print(request.form.get('materiales'))
    
    producto.tipo = request.form.get('tipo')
    producto.name = request.form.get('nameVG')
    producto.precio = request.form.get('precio')
    producto.cantidad = request.form.get('cantidad')
    producto.imagen = request.form.get('imagen')   
    producto.color = request.form.get('color')  
    producto.materiales = request.form.get('materiales')  

    #Modificamos el  producto a la base de datos.
    db.session.commit()

    return redirect(url_for('productos.consultarProductos'))

