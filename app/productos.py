from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import Productos, MateriasPrimas, UnidadDeMedida, Producto_MateriaPrima
from . import db
from .forms import RegisterProductoForm
from pprint import pprint

productos = Blueprint('productos', __name__)

@productos.route('/registerProductos')
# @login_required
def registerProductos():
    materiasU = db.session.query(MateriasPrimas, UnidadDeMedida).join(UnidadDeMedida).filter(MateriasPrimas.status==1).all()
    materiasU_list = [(materias_primas.id, '{} - {}'.format(materias_primas.nombre, materias_primas.unidadDeMedida.nombre)) for materias_primas, unidadDeMedida in materiasU]
    registerProducto = RegisterProductoForm()
    registerProducto.materiaPri.choices = materiasU_list
    context = {"registerProducto_Form": registerProducto}
    return render_template('/registerProductos.html', form = registerProducto, **context)

@productos.route('/registerProductos', methods=['POST'])
# @login_required
def registerProductos_post():
    data = request.get_json(force=True)
    materias = data.get('materias', '')
    pprint(data)
    producto = Productos()
    producto.tipo = data.get('tipo', '')
    producto.name = data.get('nombre', '')
    producto.color = data.get('color', '')
    producto.precio = float(data.get('precio', ''))
    producto.cantidad = 0
    producto.imagen = data.get('imagen', '')
    producto.materiales = ''
    producto.status = 1
    materiasIds = []
    # Obtiene los ids de materias primas para buscar
    for materia in materias:
        materiasIds.append(int(materia.get('idMateriaPri', '')))
    i= 0
    for materia in materias:
        # mPrima_por_producto = MateriaPrimaPorProducto(cantidadMateria = float(data.get('cantidadMPri', '')), cantidadMerma = (float(data.get('cantidadMPri', '')) * 0.1))
        cantidad = materia.get('cantidadMPri')
        print(cantidad)
        producto_materiaPrima = Producto_MateriaPrima(cantidad= float(cantidad), cantidadMerma = (float(cantidad) * 0.1))
        producto_materiaPrima.materias = MateriasPrimas.query.get(int(materia.get('idMateriaPri')))
        # mPrima_por_producto.materias = MateriasPrimas.query.get(int(materia.get('idMateriaPri', '')))
        producto.materiaPrima.append(producto_materiaPrima)
        db.session.commit()
        i = i +1
    
    db.session.commit()
    #lastProd_id = producto.id
    # mPrima_por_producto.producto.append(producto)
    # db.session.commit()
    return redirect(url_for('productos.consultarProductos'))

@productos.route('/consultarProductos')
# @login_required #Parar proteger la ruta, con inicio de sesion
def consultarProductos():
    #todosProductos = db.session.query(Productos).all()
    todosProductos = Productos.query.filter(status=1).all()
    productos = db.session.query(Productos, MateriasPrimas).join(MateriasPrimas).filter(Productos.status==1).all()
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

@productos.route('/productosClient')
def productosClient():
    todosProductos = Productos.query.filter_by(status=1).all()
    return render_template('/productosClient.html', todosProductos= todosProductos)

@productos.route('/eliminarProducto/<int:id>')
@login_required
def eliminarProducto(id):
    producto = db.session.query(Productos).filter(Productos.id == id).first()
    producto.status=False
    db.session.commit()
    return redirect(url_for('productos.consultarProductos'))

@productos.route('/modificarProducto/<id>')
@login_required 
def modificarProducto(id):
    producto= db.session.query(Productos).filter(Productos.id == id).first()
    """ #To update materiaPrima in productos
    data = request.get_json(force=True)
    producto= Productos.query.get(int(data.get('idProducto', '')))
    materias= data.get('materias', '')
    producto.tipo= data.get('tipo', '')
    producto.name= data.get('nombre', '')
    producto.color= data.get('color', '')
    producto.precio= data.get('precio', '')
    producto.cantidad= float(data.get('cantidad', ''))
    producto.imagen= data.get('imagen', '')
    producto.materiaPrima= []# Vacia todos los registros de materiales que existen
    db.session.commit()
    for materia in materias:
        producto_materiaPrima= Producto_MateriaPrima(cantidad= float(data.get('cantidadMPri', '')), cantidadMerma= (float(data.get('cantidadMPri', '')) * 0.1))
        producto_materiaPrima.materias= MateriasPrimas.query.get(int(materia.get('idMateriaPri', '')))
        producto.materiaPrima.append(producto_materiaPrima)
        db.session.commit() 
    db.session.commit() """
    return render_template('/modificarProductos.html', producto= producto)

@productos.route('/productosClient', methods=['POST'])
@login_required
def carritoProductos_post():
    tipo = request.form.get('tipo')
    nameVG = request.form.get('nameVG')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    imagen = request.form.get('imagen')
    color = request.form.get('color')
    status = True
    producto = Productos.query.filter_by(name=nameVG).first()
    if producto:
        flash('El producto ya existe, se modifico')
        return redirect(url_for('productos.consultarProductos'))
    producto = db.session.query(Productos).filter(Productos.id == id).first()
    db.session.commit()

    return redirect(url_for('productos.productosClient'))

@productos.route('/buscarProducto', methods=['POST'])
@login_required
def buscarProducto():
    tipo = str(request.form.get('searchtipo'))
    todosProductos = Productos.query.filter_by(tipo = tipo).filter_by(status=1).all()
    return render_template('/consultarProductos.html', todosProductos= todosProductos)

@productos.route('/modificarProductos/<id>', methods=['POST'], )
@login_required
def modificarProductos_post(id):
    producto = Productos.query.get(id)
    producto.tipo = request.form.get('tipo')
    producto.name = request.form.get('nameVG')
    producto.precio = request.form.get('precio')
    producto.cantidad = request.form.get('cantidad')
    producto.imagen = request.form.get('imagen')   
    producto.color = request.form.get('color')  
    producto.materiales = request.form.get('materiales')
    db.session.commit()

    return redirect(url_for('productos.consultarProductos'))

