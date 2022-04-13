#Importamos los módulos a usar de flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
#Importamos los módulos de seguridad para las funciones hash
from werkzeug.security import generate_password_hash, check_password_hash

#Importamos el método login_required de flask_security
from flask_security import login_required
#Importamos los métodos login_user, logout_user flask_security.utils
#########################################################################################
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
##########################################################################################
#Importamos el modelo del usuario
from . models import Usuario, usuarios_roles, Role
#Importamos el objeto de la BD y userDataStore desde __init__
from . import db, userDataStore
import datetime
from pprint import pprint
#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /security para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /security/login y security/register
auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Consultamos si existe un usuario ya registrado con el email.
    user = Usuario.query.filter_by(email=email).first()

    #Verificamos si el usuario existe
    #Tomamos el password proporcionado por el usuario lo hasheamos, y lo comparamos con el password de la base de datos.
    if not user or not check_password_hash(user.contrasenia, password):
    #if not user or not user.password==encrypt_password(password):
        #Si el usuario no existe o no coinciden los passwords
        flash('El usuario y/o la contraseña son incorrectos')
        return redirect(url_for('auth.login')) #Si el usuario no existe o el password es incorrecto regresamos a login
    
    #Si llegamos a este punto sabemos que el usuario tiene datos correctos.
    #Creamos una sessión y logueamos al usuario
    # pprint(vars(user.roles))
    login_user(user, remember=remember)
    
    #obtener el id del user
    print(user.id )
    print("Esto es una prueba {}".format(current_user.id))
#   userRoles = usuarios_roles.query.filter_by(userId=user.id).first()
#   rol = Role.query.filter_by(id=userRoles.userId).first()
#   print(rol.name)
    return redirect(url_for('main.profile'))

@auth.route('/almacenista')
def almacenista():
    return render_template('consultarUsuarios.html')

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    # EDSON: descomentar lineas cuando se tengan los inputs listos en html
    #     IMPORTANTE: (verificar que coincidan los nombres de los inputs)
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
    # Parametros que se ingresan desde backend
    # La fecha actual se obtiene desde python
    fechaRegistro = datetime.date.today()
    # El status 1 siginifica que el usuario esta activo
    status=1
    """ # Parametros hardcodeados para pruebas
    email = 'edson@gmail.com'
    contrasenia = '123456'
    nombre = 'Edson'
    status = 1
    apellidoPaterno = 'Santos'
    apellidoMaterno = 'Perez'
    fechaNacimiento = '18-08-1997'
    telefono = '4771647493'
    calle = 'Del Dinar'
    numExterior = 123
    numInterior = 0
    colonia = 'Delta de Jerez'
    cp = 37545
    fechaRegistro = '30-03-2022' """

    #Consultamos si existe un usuario ya registrado con el email.
    user = Usuario.query.filter_by(email=email).first()

    if user: #Si se encontró un usuario, redireccionamos de regreso a la página de registro
        flash('El correo electrónico ya existe')
        return redirect(url_for('auth.register'))
    # Asignamos el usuario creado
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
    # EDSON: Se define qué rol tebdrá el usuario
    role = 'cliente'
    # EDSON: Se busca el rol por "name", previamente creado en __init__.py
    default_role = userDataStore.find_role(role)
    # EDSON: Se asigna el rol al usuario
    userDataStore.add_role_to_user(usuario, default_role)
    #Añadimos el nuevo usuario a la base de datos.
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sessión
    logout_user()
    return redirect(url_for('main.index'))
