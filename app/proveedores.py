
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
from . models import Proveedores
#Importamos el objeto de la BD y userDataStore desde __init__
from . import db


#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
proveedores = Blueprint('proveedores', __name__)

@proveedores.route('/registerProveedores')
@login_required #Parar proteger la ruta, con inicio de sesion
def registerProveedores():
    
    return render_template('/registerProveedores.html')

@proveedores.route('/registerProveedores', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def registerProveedores_post():
        rfc = str(request.form.get('rfc'))
        calle = str(request.form.get('calle'))
        colonia = str(request.form.get('colonia'))
        numInter = int(request.form.get('numInter'))
        numExter = int(request.form.get('numExter'))
        razonSocial = str(request.form.get('razonSocial'))
        telefono = int(request.form.get('telefono'))
        fechaRegistro = str(request.form.get('fechaRegistro'))
        status = True

        #Consultamos si existe un usuario ya registrado con el email.
        proveedor = Proveedores.query.filter_by(rfc=rfc).first()

        if proveedor: #Si se encontró un producto
            flash('El proveedor ya existe, se modifico')
            return redirect(url_for('proveedores.consultarProveedores'))

        #Si no existe, creamos un nuevo producto con sus datos.
        new_proveedor = Proveedores(rfc=rfc, calle=calle, colonia=colonia, numInter=numInter, numExter=numExter, razonSocial=razonSocial, telefono=telefono, fechaRegistro=fechaRegistro, status=status)    
        
        db.session.add(new_proveedor)
        #Añadimos el nuevo producto a la base de datos.
        db.session.commit()

        return redirect(url_for('proveedores.consultarProveedores'))

@proveedores.route('/consultarProveedores')
@login_required #Parar proteger la ruta, con inicio de sesion
def consultarProveedores():
   #todosProductos = db.session.query(Productos).all()
    todosProveedores = Proveedores.query.filter_by(status=1).all()
    return render_template('/consultarProveedores.html', todosProveedores= todosProveedores)

#Definimos la ruta para eliminar productos
@proveedores.route('/eliminarProveedor/<int:id>')
@login_required #Parar proteger la ruta, con inicio de sesion
def eliminarProveedor(id):
    proveedor = db.session.query(Proveedores).filter(Proveedores.id == id).first()
    proveedor.status=False
    db.session.commit()
    return redirect(url_for('proveedores.consultarProveedores'))

#Definimos la ruta para modificar productos
@proveedores.route('/modificarProveedor/<id>')
@login_required #Parar proteger la ruta, con inicio de sesion
def modificarProveedor(id):    
    proveedor = db.session.query(Proveedores).filter(Proveedores.id == id).first()  
    return render_template('/modificarProveedor.html', proveedor= proveedor)

@proveedores.route('/modificarProveedor/<id>', methods=['POST'], )
@login_required #Parar proteger la ruta, con inicio de sesion
def modificarProveedor_post(id):    
    proveedor = Proveedores.query.get(id)
    
    proveedor.rfc = request.form.get('rfc')
    proveedor.calle = request.form.get('calle')
    proveedor.colonia = request.form.get('colonia')
    proveedor.numInter = request.form.get('numInter')
    proveedor.numExter = request.form.get('numExter')
    proveedor.razonSocial = request.form.get('razonSocial')
    proveedor.telefono = request.form.get('telefono')
    proveedor.fechaRegistro = request.form.get('fechaRegistro')

    #Modificamos el  producto a la base de datos.
    db.session.commit()

    return redirect(url_for('proveedores.consultarProveedores'))


@proveedores.route('/buscarProveedor', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def buscarProveedor():
   #todosProductos = db.session.query(Productos).all()
    rfc = str(request.form.get('searchrfc'))
    todosProveedores = Proveedores.query.filter_by(rfc = rfc, status=1).all()
    
    return render_template('/consultarProveedores.html', todosProveedores= todosProveedores)