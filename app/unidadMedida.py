#Importamos los módulos a usar de flask
from contextlib import nullcontext
from multiprocessing import context
from flask import Blueprint, render_template, redirect, url_for, request, flash
from pyparsing import empty
#Importamos los módulos de seguridad para las funciones hash
from werkzeug.security import generate_password_hash, check_password_hash

#Importamos el método login_required de flask_security
from flask_security import login_required
#Importamos los métodos login_user, logout_user flask_security.utils
#########################################################################################
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password

from app.forms import UnidadMedidaForm


##########################################################################################
#Importamos el modelo del usuario
from . models import UnidadDeMedida
#Importamos el objeto de la BD y userDataStore desde __init__
from . import db


#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
unidadMedida = Blueprint('unidadMedida', __name__)


@unidadMedida.route('/registerUnidadMedida')
@login_required #Parar proteger la ruta, con inicio de sesion
def registerunidadDeMedida():
    unidadMedida_Form = UnidadMedidaForm()

    context = {
            "unidadMedida_Form": unidadMedida_Form
        }
    
    return render_template('/registerUnidadMedida.html', **context)

@unidadMedida.route('/registerUnidadMedida', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def registerunidadDeMedida_post():
        unidadMedida_Form = UnidadMedidaForm()

        context = {
            "unidadMedida_Form": unidadMedida_Form
        }

        if unidadMedida_Form.validate_on_submit:
            nombre = unidadMedida_Form.nombre.data
            unidad = unidadMedida_Form.unidad.data
            status = True


        #Consultamos si existe un usuario ya registrado con el email.
        unimedidac = UnidadDeMedida.query.filter_by(nombre=nombre).first()

        if unimedidac: #Si se encontró un producto
            flash('La unidad de Medida ya existe, se modifico')
            return redirect(url_for('unidadMedida.consultarUnidadMedida'))

        #Si no existe, creamos un nuevo producto con sus datos.
        new_unidadMedida = UnidadDeMedida(nombre=nombre, unidad=unidad ,status=status)    
        
        db.session.add(new_unidadMedida)
        #Añadimos el nuevo producto a la base de datos.
        db.session.commit()

        return redirect(url_for('unidadMedida.consultarUnidadMedida'))

@unidadMedida.route('/consultarUnidadMedida')
@login_required #Parar proteger la ruta, con inicio de sesion
def consultarUnidadMedida():
   #todosProductos = db.session.query(Productos).all()
    todosUnidadMedida = UnidadDeMedida.query.filter_by(status=1).all()
    return render_template('/consultarUnidadMedida.html', todosUnidadMedida= todosUnidadMedida)

#Definimos la ruta para eliminar productos
@unidadMedida.route('/eliminarUnidadMedida/<int:id>')
@login_required #Parar proteger la ruta, con inicio de sesion
def eliminarUnidadMedida(id):
    UnidadMedida = db.session.query(UnidadDeMedida).filter(UnidadDeMedida.id == id).first()
    UnidadMedida.status=False
    db.session.commit()
    return redirect(url_for('unidadMedida.consultarUnidadMedida'))

#Definimos la ruta para modificar productos
@unidadMedida.route('/modificarUnidadMedida/<id>')
@login_required #Parar proteger la ruta, con inicio de sesion
def modificarUnidadMedida(id):    
    unidadMedidas = UnidadDeMedida.query.get(id)

    unidadMedidas_Form = UnidadMedidaForm()

    context = {
        "unidadMedida_Form": unidadMedidas_Form
    }

    unidadMedidas.nombre = unidadMedidas_Form.nombre.data
    
    unidadMedidas.unidad = unidadMedidas_Form.unidad.data  

    return render_template('/modificarUnidadMedida.html', UnidadMedidas = unidadMedidas,**context)

@unidadMedida.route('/modificarUnidadMedida/<id>', methods=['POST'], )
@login_required #Parar proteger la ruta, con inicio de sesion
def modificarUnidadMedida_post(id):    
    unidadMedidas = UnidadDeMedida.query.get(id)
    unidadMedidas_Form = UnidadMedidaForm()

    context = {
        "unidadMedida_Form": unidadMedidas_Form
    }

    unidadMedidas.nombre = unidadMedidas_Form.nombre.data
    print(unidadMedidas_Form.nombre.data)
    unidadMedidas.unidad = unidadMedidas_Form.unidad.data
    print(unidadMedidas_Form.unidad.data)

    #Modificamos el  producto a la base de datos.
    db.session.commit()

    return redirect(url_for('unidadMedida.consultarUnidadMedida'))


@unidadMedida.route('/buscarUnidadMedida', methods=['POST'])
@login_required #Parar proteger la ruta, con inicio de sesion
def buscarUnidadMedida():
   #todosProductos = db.session.query(Productos).all()  
    nombre = str(request.form.get('searchnombre'))
    print(nombre)
    print(str(request.form.get('searchnombre')))
    todosUnidadMedida = UnidadDeMedida.query.filter_by(nombre = nombre).filter_by(status=1).all()
    
    return render_template('/consultarUnidadMedida.html', todosUnidadMedida= todosUnidadMedida)