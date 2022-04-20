from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, DateField, IntegerField
from wtforms import FloatField, SelectField, StringField, SubmitField
from wtforms import FileField
# from wtforms.fields import StringField, IntegerField, RadioField
from wtforms import validators
from wtforms.validators import DataRequired
from . models import UnidadDeMedida

class RegisterUserForm(FlaskForm):
    """ matricula=StringField('matricula', validators=[DataRequired()])
    grupo=StringField('grupo', validators=[DataRequired()])
    nombre=StringField('nombre',  validators=[DataRequired()])
    apaterno=StringField('apaterno', validators=[DataRequired()])
    amaterno=StringField('amaterno', validators=[DataRequired()])
    sexo=RadioField('sexo',choices=[('M','Masculino'),('F','Femenino')])
    dia=StringField('dia', validators=[DataRequired()])
    mes=StringField('mes', validators=[DataRequired()])
    anio=StringField('año', validators=[DataRequired()]) """

    email=EmailField('CORREO ELECTRONICO(*):', validators =[DataRequired(message='El dato es obligatiorio'), validators.Email(message='Introduce un email válido')])
    password=PasswordField('CONTRASEÑA(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    nombre=StringField('NOMBRE (*)', validators=[DataRequired(message='El dato es obligatiorio')])
    apellidoPaterno=StringField('APELLIDO PATERNO(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    apellidoMaterno=StringField('APELLIDO MATERNO(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    fechaNacimiento=DateField('FECHA DE NACIMIENTO(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    telefono=StringField('NUMERO TELEFONICO(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    calle=StringField('CALLE(*):', validators=[DataRequired(message='El dato es obligatiorio')],)
    numExterior=IntegerField('NUMERO EXTERIOR(*):', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=0, message='El numero exterior no puede ser menor a 0')])
    numInterior=IntegerField('NUMERO INTERIOR:', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=0, message='El numero interior no puede ser menor a 0')])
    colonia=StringField('COLONIA(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    cp=IntegerField('CODIGO POSTAL(*):', validators=[DataRequired(message='El dato es obligatiorio')])
    submit=SubmitField()

class RegisterMateriaPrimaForm(FlaskForm):
    nombre=StringField('Nombre', validators=[DataRequired(message='El dato es obligatiorio')], id='nombreMateria', name='nombreMateria')
    cantidad=IntegerField('Cantidad', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=1, message='El valor minimo es 1')], id='cantidadMateria', name='cantidadMateria')
    u_medida=SelectField('Unidad de medida', choices=[], validators=[DataRequired(message='El dato es obligatiorio')], id='unidadMedida', name='unidadMedida')

""" INTEGRACION GAEL """
class UnidadMedidaForm(FlaskForm):
    nombre = StringField("Nombre de la Unidad de Medida:", validators=[DataRequired(message='El dato es obligatiorio'), validators.length(max=30)])
    unidad = FloatField("Unidad de conversion, considerar la unidad mas pequeña (gramos,mililtros,piezas...)", validators=[DataRequired(message='El dato es obligatiorio')])

class RegisterCompraForm(FlaskForm):
    proveedor=SelectField('Prooveedor', choices=[], validators=[DataRequired(message='El dato es obligatiorio')], id='proveedorCompra', name='proveedorCompra')
    cantidad=IntegerField('Cantidad de materia prima', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=1, message='El valor minimo es 1')], id='cantidadMateriaCompra', name='cantidadMateriaCompra')
    materiaPri=SelectField('Materia Prima', choices=[], validators=[DataRequired(message='El dato es obligatiorio')], id='materiaPriCompra', name='materiaPriCompra')
    precioU=FloatField('Precio Unitario', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=0.5, message='El valor minimo es 1')], id='precioUMateria', name='precioUMateria')

class RegisterPedidoForm(FlaskForm):
    cantidad=IntegerField('Cantidad de producto', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=1, message='El valor minimo es 1')], id='cantidadProducto', name='cantidadProducto')
    productoPedido=SelectField('Productos', choices=[], validators=[DataRequired(message='El dato es obligatiorio')], id='productoPedido', name='productoPedido')

class RegisterProductoForm(FlaskForm):
    tipo=SelectField('Tipo producto', choices=[('bolso', 'Bolso'), ('cartera', 'Cartera'), ('cinto', 'Cinto')], validators=[DataRequired(message='El dato es obligatiorio')], id='tipoProducto', name='tipoProducto')
    nombre = StringField("Nombre:", validators=[DataRequired(message='El dato es obligatiorio'), validators.length(max=50)], id='nombreProducto', name='nombreProducto')
    imagen = FileField("Imagen:", validators=[DataRequired(message='El dato es obligatiorio')],  id='imagenProducto', name='imagenProducto')
    color=SelectField('Color', choices=[('cafe', 'Café'), ('negro', 'Negro')], validators=[DataRequired(message='El dato es obligatiorio')], id='colorProducto', name='colorProducto')
    # cantidad=IntegerField('Cantidad en stock', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=1, message='El valor minimo es 1')], id='cantidadStock', name='cantidadStock')
    cantidadMPri=IntegerField('Cantidad de materia prima', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=1, message='El valor minimo es 1')], id='cantidadMPri', name='cantidadMPri')
    materiaPri=SelectField('Materia Prima', choices=[], validators=[DataRequired(message='El dato es obligatiorio')], id='materiaPriProducto', name='materiaPriProducto')
    precio=FloatField('Precio', validators=[DataRequired(message='El dato es obligatiorio'), validators.number_range(min=0.5, message='El valor minimo es 1')], id='precioProducto', name='precioProducto')