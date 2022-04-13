#Importamos los módulos a usar de flask

from flask import Blueprint, render_template, redirect, url_for, request, flash
#Importamos los módulos de seguridad para las funciones hash
from werkzeug.security import generate_password_hash, check_password_hash

#Importamos el método login_required de flask_security
from flask_security import login_required, roles_accepted
#Importamos los métodos login_user, logout_user flask_security.utils
#########################################################################################
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
##########################################################################################
#Importamos el modelo del usuario
from . models import Productos
#Importamos el objeto de la BD y userDataStore desde __init__
from . import db, userDataStore
from . models import Usuario, usuarios_roles, Role, Proveedores, MateriasPrimas, UnidadDeMedida
import datetime
# current_user tiene un metodo .has_role('role_name') para conocer el rol del un usuario
from flask_security import current_user
from .forms import RegisterCompraForm

#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
almacenistas = Blueprint('almacenistas', __name__)

@almacenistas.route('/listarUsuarios')
@login_required
# @roles_accepted('admin', 'almacenista')
def listar():
    # print(current_user.has_role('almacenista'))
    users = Usuario.query.filter_by(status=1).all()
    print(current_user.id)
    return render_template('administrarAlmacenista.html', todosUsuarios = users)

@almacenistas.route('/agregarUsuario', methods=['POST'])
@login_required
# @roles_accepted('admin', 'almacenista')
def agregarUsuario():
    email = request.form.get('email')
    contrasenia = request.form.get('password')
    nombre = request.form.get('nombre')
    apellidoPaterno = request.form.get('apellidoPaterno')
    apellidoMaterno = request.form.get('apellidoMaterno')
    fechaNacimiento = datetime.datetime.strptime(request.form.get('fechaNacimiento'), '%Y-%m-%d')
    telefono = request.form.get('telefono')
    calle = request.form.get('calle')
    numExterior = request.form.get('numExterior')
    numInterior = request.form.get('numInterior')
    colonia = request.form.get('colonia')
    cp = request.form.get('cp')
    fechaRegistro = datetime.date.today()
    status=1
    user = Usuario.query.filter_by(email=email).first()
    if user:
        flash('El correo electrónico ya existe')
        return redirect(url_for('auth.register'))
    usuario = userDataStore.create_user(
    email = email,
    contrasenia = generate_password_hash(contrasenia, method='sha256'),
    nombre = nombre,
    status = status,
    apellidoPaterno = apellidoPaterno,
    apellidoMaterno = apellidoMaterno,
    fechaNacimiento = fechaNacimiento,
    telefono = telefono,
    calle = calle,
    numExterior = numExterior,
    numInterior = numInterior,
    colonia = colonia,
    cp = cp,
    fechaRegistro = fechaRegistro)
    role = 'almacenista'
    default_role = userDataStore.find_role(role)
    userDataStore.add_role_to_user(usuario, default_role)
    db.session.commit()
    return redirect(url_for('almacenistas.listar'))

@almacenistas.route('/editarUsuario/<id>', methods=['POST'])
@login_required
# @roles_accepted('admin', 'almacenista')
def editarAlmacenista(id):
    usuario = Usuario.query.get(id)
    usuario.email = request.form.get('email')
    usuario.contrasenia = request.form.get('password')
    usuario.nombre = request.form.get('nombre')
    usuario.apellidoPaterno = request.form.get('apellidoPaterno')
    usuario.apellidoMaterno = request.form.get('apellidoMaterno')
    usuario.fechaNacimiento = datetime.datetime.strptime(request.form.get('fechaNacimiento'), '%Y-%m-%d')
    usuario.telefono = request.form.get('telefono')
    usuario.calle = request.form.get('calle')
    usuario.numExterior = request.form.get('numExterior')
    usuario.numInterior = request.form.get('numInterior')
    usuario.colonia = request.form.get('colonia')
    usuario.cp = request.form.get('cp')
    db.session.commit()
    return redirect(url_for('almacenistas.listar'))

@almacenistas.route('/eliminarUsuario/<id>')
@login_required
# @roles_accepted('admin', 'almacenista')
def eliminarAlmacenista(id):
    usuario = Usuario.query.get(id)
    if usuario != current_user:
        usuario.status = 0
        usuario.active = False
        db.session.commit()
    else:
        flash('No se puede eliminar el perfil activo')
        print('No se puede eliminar el perfil activo')
    return redirect(url_for('almacenistas.listar'))

""" @almacenistas.route('/compras')
# @roles_accepted('admin', 'almacenista')
def listarCompras():
    proveedores = Proveedores.query.filter_by(status=1).all()
    materias = MateriasPrimas.query.filter_by(status=1).all()
    materiasU = db.session.query(MateriasPrimas, UnidadDeMedida).join(UnidadDeMedida).filter(MateriasPrimas.status==1).all()
    proveedores_list = [(i.id, i.razonSocial) for i in proveedores]
    materias_list = [(i.id, i.nombre) for i in materias]
    materiasU_list = [(materias_primas.id, '{} - {}'.format(materias_primas.nombre, materias_primas.unidadDeMedida.nombre)) for materias_primas, unidadDeMedida in materiasU]
    registerCompraForm = RegisterCompraForm()
    registerCompraForm.proveedor.choices = proveedores_list
    registerCompraForm.materiaPri.choices = materiasU_list
    context = {"registerCompra_Form": registerCompraForm}
    return render_template('administrarCompras.html', form = registerCompraForm, **context)

@almacenistas.route('/crearCompra', methods=['POST'])
# @roles_accepted('admin', 'almacenista')
def crearCompra():
    data = request.get_json(force=True)
    print(data)
    return data """
