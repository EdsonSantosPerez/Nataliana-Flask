""" IMPORTANTE: para correr el proyecto => set FLASK_APP=app\ """
#Archivo de configuración que tiene la función de crear nuestra aplicación, iniciar la base de datos y registrará nuestros modelos.
import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#Importamos las clases de User y Role del modelo
from .models import Usuario, Role, Productos
#Creamos un objeto de la clase SQLAlchemySessionUserDatastore
userDataStore = SQLAlchemyUserDatastore(db, Usuario, Role )

productoDataStore = SQLAlchemyUserDatastore(db, Usuario, Role )

#Método de inicio de la aplicación
def create_app():
    #Creamos una instancia de la clase Flask
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    app.config['SECRET_KEY'] = os.urandom(24)
    #Definimos la ruta a la BD: mysql://user:password@localhost/bd'
    """ EDSON: En mi caso tuve agregarle el puerto a "localhost" (:3307) porque corresponde a mi conexion de MySQL Workbench """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3307/natalianaDB'
    # We're using PBKDF2 with salt.
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    #Semilla para el método de encriptado que utiliza flask-security
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    #Inicializamos y creamos la BD
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
        # EDSON: Se crean los roles que la aplicación manejará
        userDataStore.find_or_create_role(name='admin', rol='ADMIN')
        userDataStore.find_or_create_role(name='almacenista', rol='ALMACENISTA')
        userDataStore.find_or_create_role(name='cliente', rol='CLIENTE')
        db.session.commit()

    #Conectando los modelos a fask-security usando SQLAlchemyUserDatastore
    security = Security(app, userDataStore)
    #Registramos el blueprint para las rutas auth de la aplicación
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Registramos el blueprint para las partes no auth de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    #Registramos el blueprint para productos
    from .productos import productos as productos_blueprint
    app.register_blueprint(productos_blueprint)
    
    #Registramos el blueprint para productos
    from .proveedores import proveedores as proveedores_blueprint
    app.register_blueprint(proveedores_blueprint) 

    from .almacenistas import almacenistas as almacenistas_blueprint
    app.register_blueprint(almacenistas_blueprint)

    from .materias_primas import materias_primas as materias_primas_blueprint
    app.register_blueprint(materias_primas_blueprint)

    from .unidadMedida import unidadMedida as unidadMedida_blueprint
    app.register_blueprint(unidadMedida_blueprint)

    from .compras import compras as compras_blueprint
    app.register_blueprint(compras_blueprint)

    from .pedidos import pedidos as pedidos_blueprint
    app.register_blueprint(pedidos_blueprint)

    return app
