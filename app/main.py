#Importamos la clase Blueprint del módulo flask
from flask import Blueprint, render_template
#Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required
#Importamos el objeto de la BD desde __init__.py
from . import db
from flask_security import current_user

main = Blueprint('main',__name__)

#Definimos la ruta a la página principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
def profile():
    print(current_user.has_role('cliente'))
    return render_template('index.html', name=current_user.nombre)




