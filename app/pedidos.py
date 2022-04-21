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
    materias = MateriasPrimas.query.filter_by(status=1).all()
    materiasProductos = []
    haySuficienteMaterial = False
    for producto in productos:
        productosMaterias= db.session.query(Productos, Producto_MateriaPrima).join(Producto_MateriaPrima).filter(Producto_MateriaPrima.idProducto == int(producto.get('idProducto', ''))).all()
        for productos, producto_materia_prima in productosMaterias:
            """ print('----------- productos -----------')
            pprint(vars(productos)) 
            print('----------- producto_materia_prima -----------')
            pprint(vars(producto_materia_prima))
            print('----------- producto_materia_prima.cantidad + producto_materia_prima.cantidadMerma -----------')
            print((producto_materia_prima.cantidad + producto_materia_prima.cantidadMerma)) """
            res= next((item for item in materiasProductos if item["idMaterial"] == producto_materia_prima.idMateriaPr), False)
            """ print('-------- res --------')
            print(res) """
            if res == False:
                materiasProductos.append({'idMaterial': producto_materia_prima.idMateriaPr, 'cantidadPedidoTotal': (producto_materia_prima.cantidad + producto_materia_prima.cantidadMerma)})
            else:
                i= next((index for (index, d) in enumerate(materiasProductos) if d["idMaterial"] == producto_materia_prima.idMateriaPr), False)
                # print('{} + {}'.format(materiasProductos[i]['cantidadPedidoTotal'], (producto_materia_prima.cantidad + producto_materia_prima.cantidadMerma)))
                materiasProductos[i]['cantidadPedidoTotal'] += (producto_materia_prima.cantidad + producto_materia_prima.cantidadMerma)
            """ print('------------------ materiasProductos Array ------------------')
            print(materiasProductos) """

    print('------------------ materiasProductos Array FINAL ------------------')
    print(materiasProductos)
        # pedido_productos= ProductosPedido(cantidad = producto.get('cantidadProducto', ''))
        # pedido_productos.producto= Productos.query.get(int(producto.get('idProducto', '')))
    
        # db.session.commit()
    for materia in materiasProductos:
        materiaPri= MateriasPrimas.query.get(int(materia['idMaterial']))
        if materiaPri.cantidad >= materia['idMaterial']:
            haySuficienteMaterial = True
        else:
            haySuficienteMaterial = False
    # db.session.commit()
    print(haySuficienteMaterial)
    return '{}'.format(haySuficienteMaterial)