from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.forms.models import model_to_dict
from datetime import datetime
from .choise import gender_choices

class UsuarioManager(BaseUserManager):
    def create_user(self,email,username,nombres,apellidos,password = None):
        if not email:
            raise ValueError('El usuario necesita correo electronico')
        user=self.model( 
            username=username,
            email=self.normalize_email(email),
            nombres=nombres,
            apellidos=apellidos

        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,email,nombres,apellidos,password):
        user=self.create_user(
            email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password
        )
        user.usuario_administrador = True
        user.save()
        return user        

class Usuario(AbstractBaseUser,PermissionsMixin):
    username=models.CharField('Nombre de usuario',unique=True,max_length=100)
    email=models.EmailField('Correo Electrónico',max_length=254,unique=True)
    nombres=models.CharField('Nombres',max_length=200,blank=True,null=True)
    apellidos=models.CharField('Apellidos',max_length=200,blank=True,null=True)
    dni=models.IntegerField(unique=True,blank=True,null=True)
    salario=models.FloatField(blank=True,null=True)
    admin=models.BooleanField(default=False,null=True,blank=True)
    usuario_activo=models.BooleanField(default=True)
    usuario_administrador=models.BooleanField(default=False)
    objects=UsuarioManager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email','nombres','apellidos']
    def __str__(self):
        return f'{self.nombres},{self.apellidos}'
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True    
    @property
    def is_staff(self):
        return self.usuario_administrador   




class vendedor(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    Telefono=models.IntegerField()
    sucursal=models.CharField(unique=True,max_length=100)
    sueldo=models.FloatField()
    NroProductoVendidos=models.IntegerField()
    class Meta:
        verbose_name='Vendedor'
        verbose_name_plural='Vendedores'
        ordering=['user']
    def __str__(self):
        return f'{self.user}'




class Salario(models.Model):
    nombre=models.CharField(max_length=200)
    class Meta:
        verbose_name='Salario'
        verbose_name_plural='Salarios'
        ordering=['nombre']    
    def __str__(self):
        return f'{self.nombre}'
 

    

class Administrador(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion=models.TextField()
    numeroTelefono=models.IntegerField()
    class Meta:
        verbose_name='Administrador'
        verbose_name_plural='Administradores'
        ordering=['user']
    def __str__(self):
        return f'{self.user}'

class Sucursal(models.Model):
   id=models.AutoField(primary_key=True)
   ciudad=models.CharField(max_length=200)
   direccion=models.CharField(max_length=200)
   ganancia=models.FloatField()
   class Meta:
        verbose_name='Sucursal'
        verbose_name_plural='Sucursales'
        ordering=['ciudad']
   def __str__(self):
        return f'{self.ciudad}'





class Categoria(models.Model):
   idCategoria = models.AutoField(primary_key=True)
   nombrecategoria=models.CharField(unique=True,max_length=100)
   dscripcionCategoria=models.TextField(null=False)

   def toJSON(self):
        item = model_to_dict(self)
        return item

   class Meta:
        verbose_name='Categoria'
        verbose_name_plural='Categorias'
        ordering=['nombrecategoria']
   def __str__(self):
        return f'{self.nombrecategoria}'







class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombre=models.CharField('NombreP',null=False,unique=True,max_length=100)
    caracteristicas=models.TextField(null=False)
    cantidad=models.IntegerField()
    precio=models.FloatField()
    impuestos=models.FloatField()
    descuentoPorc=models.FloatField()
    ubicacionTienda=models.CharField(max_length=200)
    disponible=models.BooleanField(default=True)
    sucursal=models.ForeignKey(Sucursal,null=True,on_delete=models.CASCADE)
    categoria=models.ForeignKey(Categoria,null=True,on_delete=models.CASCADE)
     
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = {'nombre': self.nombre}
        item['categoria'] = self.categoria.toJSON()
        
        return item
          

    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering=['nombre']

    def __str__(self):
        return f'{self.nombre}'
   




class Proveedor(models.Model):
   id= models.AutoField(primary_key=True)
   nombres=models.CharField(max_length=150)
   apellidos=models.CharField(max_length=150)
   ciudad=models.CharField(max_length=100)
   direccion=models.CharField(max_length=100)
   telefono=models.BigIntegerField(null=True)
   nombreContacto=models.CharField(max_length=100)

   class Meta:
        verbose_name='Proveedor'
        verbose_name_plural='Proveedores'
        ordering=['id']

   def __str__(self):
        return f'{self.nombres}'

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

class Sale(models.Model):
    cli = models.CharField(max_length=150, verbose_name='cliente',null=True)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.cli)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] =format(self.cli) 
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item


    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']



class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __str__(self):
        return str(self.sale.cli)
        
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']