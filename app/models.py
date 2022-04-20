from email.policy import default
from sqlalchemy import true
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

usuarios_roles = db.Table('usuarios_roles',
    db.Column('usuarioId', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('roleId', db.Integer, db.ForeignKey('role.id')))

class Usuario(db.Model, UserMixin):
    _tablename_ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    contrasenia = db.Column(db.String(255), nullable=False)
    apellidoPaterno = db.Column(db.String(255), nullable=False)
    apellidoMaterno = db.Column(db.String(255), nullable=False)
    fechaNacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(255), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    numExterior = db.Column(db.String(255), nullable=False)
    numInterior = db.Column(db.String(255), nullable=False)
    colonia = db.Column(db.String(255), nullable=False)
    cp = db.Column(db.Integer, nullable=False)
    fechaRegistro = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    # EDSON: atributo obligatorio
    active = db.Column(db.Boolean())
    roles = db.relationship('Role',
        secondary=usuarios_roles,
        backref= db.backref('usuarios', lazy='dynamic'))

class Role(RoleMixin, db.Model):
    """Role model"""

    _tablename_ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    # EDSON: atributo obligatorio
    name = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

""" INTEGRACION ADRIAN """
class Proveedores(db.Model):
    """Proveedores model"""
    
    _tablename_ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    rfc = db.Column(db.String(13), nullable=False)
    calle = db.Column(db.String(50), nullable=False)
    colonia = db.Column(db.String(50), nullable=False)
    numInter = db.Column(db.Integer, nullable=False)
    numExter = db.Column(db.Integer)
    razonSocial = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    fechaRegistro = db.Column(db.Date)
    status = db.Column(db.Boolean)

""" INTEGRACION GAEL """
class UnidadDeMedida(db.Model):
    """UnidadesDeMedida model"""
    
    _tablename_ = 'unidad_de_medida'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    unidad = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

class MateriasPrimas(db.Model):
    """MateriasPrimas model"""
    
    _tablename_ = 'materiasPrimas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    idUMedida = db.Column(db.Integer,  db.ForeignKey('unidad_de_medida.id'), nullable=False)
    unidadDeMedida = db.relationship('UnidadDeMedida', 
        backref= 'materiasPrimas', lazy=True)
    """ idProveedor = db.Column(db.Integer,  db.ForeignKey('proveedores.id'), nullable=False)
    proveedor = db.relationship('Proveedores', 
        backref= 'materiasPrimas', lazy=True) """

class Producto_MateriaPrima(db.Model):
    _tablename_ = 'producto_materiaPrima'

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)
    cantidadMerma = db.Column(db.Float, nullable=False)
    idMateriaPr = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.id'))
    producto = db.relationship('Productos',
        backref= db.backref('producto_materiaprimas', lazy=True))
    materias = db.relationship('MateriasPrimas',
        backref= db.backref('producto_materiaprimas', lazy=True))


class Productos(db.Model):
    """Productos model"""
    
    _tablename_ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float)
    cantidad = db.Column(db.Integer)
    imagen = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean)
    materiaPrima = db.relationship('Producto_MateriaPrima',
        backref= db.backref('productoMatPri', lazy=True))

""" productos_pedidos = db.Table('productos_pedidos',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('pedidoId', db.Integer, db.ForeignKey('pedidos.id')),
    db.Column('productoId', db.Integer, db.ForeignKey('productos.id'))) """

class ProductosPedido(db.Model):

    _tablename_ = 'productos_pedidos'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    pedidoId = db.Column(db.Integer, db.ForeignKey('pedidos.id'))
    productoId = db.Column(db.Integer, db.ForeignKey('productos.id'))
    producto = db.relationship('Productos',
        backref= db.backref('pedido_producto', lazy=True))
    pedido = db.relationship('Pedidos',
        backref= db.backref('pedido_producto', lazy=True))

class Pedidos(db.Model):

    """Pedidos Model"""

    _tablename_ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    codigoPedido=db.Column(db.String(50), nullable=False)
    fechaPedido = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean)
    # idProducto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    productos = db.relationship('ProductosPedido',
        backref= db.backref('pedidoProductos', lazy=True))

ventas_productos = db.Table('ventas_productos',
    db.Column('cantidad', db.Integer, nullable=False),
    db.Column('productoId', db.Integer, db.ForeignKey('productos.id')),
    db.Column('ventaId', db.Integer, db.ForeignKey('ventas.id')))

class Ventas(db.Model):

    """Ventas Model"""

    _tablename_ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    precio_total=db.Column(db.Float)
    fechaRegistro = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean)
    idUsuario = db.Column(db.Integer, db.ForeignKey('productos.id'))
    productos = db.relationship('Productos',
        secondary=ventas_productos,
        backref= db.backref('ventas', lazy='dynamic'))

""" compra_materiaPrima = db.Table('usuarios_roles',
    db.Column('usuarioId', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('roleId', db.Integer, db.ForeignKey('role.id'))) """

""" compra_materiaprima = db.Table('compra_materiaprima',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('precioUnitario', db.Float, nullable=False),
    db.Column('cantidad', db.Integer, nullable=False),
    db.Column('fechaRegistro', db.String(50), nullable=False),
    db.Column('idMateriaPrima', db.Integer, db.ForeignKey('materias_primas.id')),
    db.Column('idCompra', db.Integer, db.ForeignKey('compras.id'))) """

class Compra_MateriaPrima(db.Model):
    """Compras Model"""

    __tablename__='compra_materiaprima'
    id = db.Column(db.Integer, primary_key=True)
    precioUnitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fechaRegistro = db.Column(db.String(50), nullable=False)
    idMateriaPrima = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    idCompra = db.Column(db.Integer, db.ForeignKey('compras.id'))
    compra = db.relationship('Compras',
        backref= db.backref('compra_materiaprimas', lazy=True))
    materias = db.relationship('MateriasPrimas',
        backref= db.backref('compra_materiaprimas', lazy=True))

class Compras(db.Model):
    """Compras Model"""

    __tablename__='compras'
    id = db.Column(db.Integer, primary_key=True)
    precioTotal = db.Column(db.Float, nullable=False)
    fechaCompra = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean)
    idProveedores = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    proveedores = db.relationship('Proveedores',
        backref= db.backref('comprasProv', lazy=True))
    materias = db.relationship('Compra_MateriaPrima',
        backref= db.backref('compraMatPri', lazy=True))

""" class MateriaPrimaPorProducto(db.Model):

    __tablename__='materia_prima_por_producto'
    id = db.Column(db.Integer, primary_key=True)
    cantidadMateria = db.Column(db.Float, nullable=False)
    cantidadMerma = db.Column(db.Float, nullable=False)
    idMateriaPr = db.Column(db.Integer, db.ForeignKey('materias_primas.id'))
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.id'))
    producto = db.relationship('Productos',
        backref= db.backref('materias_primas_por_productos', lazy=True))
    materias = db.relationship('MateriasPrimas',
        backref= db.backref('materias_primas_por_productos', lazy=True)) """

