from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, roles_accepted
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import Productos, MateriasPrimas
from . import db, userDataStore
import datetime
from flask_security import current_user
from .forms import RegisterProductoForm

pedidos = Blueprint('pedidos', __name__)

@pedidos.route('/crearForm')
@login_required
def crearForm():
    productos = Productos.query.filter_by(status=1).all()
    productos_list = [(i.id, i.name) for i in productos]
    registerPedidoForm = RegisterProductoForm()
    registerPedidoForm.productoPedido.choices = productos_list
    context = {"registerPedido_Form": registerPedidoForm}
    return render_template('administrarPedidos.html', form = registerPedidoForm, **context)

""" IMPORTANTE: actualizar en tabla materias primas el nuevo stock de la compra """

@pedidos.route('/crear', methods=['POST'])
@login_required
def crearCompra():
    data = request.get_json(force=True)
    # obtiene el valor del json
    materias = data.get('materias', '')
    compra = Compras()
    compra.fechaCompra = datetime.date.today()
    compra.status = 1
    compra.idProveedores = int(data.get('idProveedor', ''))
    compra.precioTotal = 0
    total = 0
    materiasIds = []
    # Obtiene los ids de materias primas para buscar
    for materia in materias:
        materiasIds.append(int(materia.get('idMateriaPri', '')))
    i= 0
    for materia in materias:
        compra_Materia = Compra_MateriaPrima(
            precioUnitario = float(materia.get('precioU', '')),
            cantidad = materia.get('cantidad', ''),
            fechaRegistro=datetime.date.today()
        )
        total += (float(materia.get('precioU', '')) * int(materia.get('cantidad', '')))
        compra_Materia.materias= MateriasPrimas.query.get(materiasIds[i])
        compra.materias.append(compra_Materia)
        db.session.commit()
        i = i +1
    
    compra.precioTotal = total
    db.session.commit()
    return data