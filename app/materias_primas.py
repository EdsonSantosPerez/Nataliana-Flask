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
from . models import Usuario, usuarios_roles, Role, MateriasPrimas, UnidadDeMedida
import datetime
from app.forms import RegisterMateriaPrimaForm
# current_user tiene un metodo .has_role('role_name') para conocer el rol del un usuario
from flask_security import current_user

#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
materias_primas = Blueprint('materias_primas', __name__)

@materias_primas.route('/listarMateriasPrimas')
@login_required
# @roles_accepted('admin', 'almacenista')
def listar():
    umedidas = UnidadDeMedida.query.filter_by(status=1).all()
    materias = db.session.query(MateriasPrimas, UnidadDeMedida).join(UnidadDeMedida).filter(MateriasPrimas.status==1).all()
    medida_list=[(i.id, i.nombre) for i in umedidas]
    materiaPrimaForm = RegisterMateriaPrimaForm()
    materiaPrimaForm.u_medida.choices = medida_list
    context = {"materiaPrima_Form": materiaPrimaForm}
    # materias = MateriasPrimas.query(MateriasPrimas, UnidadDeMedida).join(UnidadDeMedida).all()
    return render_template('administrarMateriasPrimas.html', form=materiaPrimaForm,todosMedidas= umedidas, todosMaterias = materias, **context)

@materias_primas.route('/agregarMateria', methods=['POST'])
@login_required
# @roles_accepted('admin', 'almacenista')
def agregarMateria():
    umedidas = UnidadDeMedida.query.filter_by(status=1).all()
    medida_list=[(i.id, i.nombre) for i in umedidas]
    materiaPrimaForm = RegisterMateriaPrimaForm()
    materiaPrimaForm.u_medida.choices = medida_list
    """ nombreMateria=''
    cantidad=0
    idUMedida=0
    status= True """
    if materiaPrimaForm.nombre.data and materiaPrimaForm.cantidad.data and materiaPrimaForm.u_medida.data:
        """ nombreMateria=materiaPrimaForm.nombre.data
        cantidad=materiaPrimaForm.cantidad.data
        idUMedida=materiaPrimaForm.u_medida.data
        status=True """
        new_materia = MateriasPrimas(nombre=materiaPrimaForm.nombre.data, cantidad=materiaPrimaForm.cantidad.data, status=True, idUMedida=materiaPrimaForm.u_medida.data)
        db.session.add(new_materia)
        db.session.commit()
    return redirect(url_for('materias_primas.listar'))

@materias_primas.route('/editarMateria/<id>', methods=['POST'])
@login_required
# @roles_accepted('admin', 'almacenista')
def editarMateria(id):
    materia = MateriasPrimas.query.get(id)
    materiaPrimaForm = RegisterMateriaPrimaForm()
    if materiaPrimaForm.nombre.data and materiaPrimaForm.cantidad.data and materiaPrimaForm.u_medida.data:
        materia.nombre = materiaPrimaForm.nombre.data
        materia.cantidad = materiaPrimaForm.cantidad.data
        materia.idUMedida = materiaPrimaForm.u_medida.data
        db.session.commit()
    return redirect(url_for('materias_primas.listar'))

@materias_primas.route('/eliminarMateria/<id>')
@login_required
# @roles_accepted('admin', 'almacenista')
def eliminarAlmacenista(id):
    materia = MateriasPrimas.query.get(id)
    materia.status = 0
    db.session.commit()
    return redirect(url_for('materias_primas.listar'))