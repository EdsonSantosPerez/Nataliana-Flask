from flask import Blueprint, render_template, redirect, url_for, request
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import Productos, MateriasPrimas, Pedidos, ProductosPedido, Producto_MateriaPrima
from . import db
import datetime
from flask_security import current_user
from .forms import RegisterPedidoForm
from pprint import pprint

pedidos = Blueprint('pedidos', __name__)

@pedidos.route('/crearFormPedido')
# @login_required
def crearForm():
    productos = Productos.query.filter_by(status=1).all()
    productos_list = [(i.id, i.name) for i in productos]
    registerPedidoForm = RegisterPedidoForm()
    registerPedidoForm.productoPedido.choices = productos_list
    context = {"registerPedido_Form": registerPedidoForm}
    return render_template('administrarPedidos.html', form = registerPedidoForm, **context)

@pedidos.route('/crearPedido', methods=['POST'])
# @login_required
def crearPedido():
    data = request.get_json(force=True)
    productos = data.get('productos', '')
    pedido = Pedidos(codigoPedido= 'uuid', fechaPedido= datetime.date.today(), status=1)
    # Obtiene los ids de materias primas para buscar
    existeMaterial= False
    materiasProductos = []
    for producto in productos:
        productosMaterias= db.session.query(Productos, Producto_MateriaPrima).join(Producto_MateriaPrima).filter(Producto_MateriaPrima.idProducto == int(producto.get('idProducto', ''))).all()
        print('----------- productosMaterias -----------')
        pprint(productosMaterias)
        for productos, producto_materia_prima in productosMaterias:
            print('----------- productos -----------')
            pprint(productos)
            print('----------- producto_materia_prima -----------')
            pprint(producto_materia_prima)
            # materiasProductos.append({'idMaterial': 0, 'cantidadPedidoTotal':0})
        # pedido_productos= ProductosPedido(cantidad = producto.get('cantidadProducto', ''))
        # pedido_productos.producto= Productos.query.get(int(producto.get('idProducto', '')))
        
        # db.session.commit()
    
    # db.session.commit()
    return data