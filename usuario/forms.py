from django.forms import *
from django import forms
from datetime import datetime
from .models import Producto,Sucursal,Categoria,Proveedor,DetSale
from django .contrib.auth.forms import AuthenticationForm
from .models import Usuario,Sale,Client
from django.contrib.auth.models import Group


import django_filters


class FormularioUsuario(forms.ModelForm):
    password1=forms.CharField(label='Contraseña',widget=forms.PasswordInput(

        attrs = {
            'class':'form-control',
            'placeholder':'Ingrese su contraseña',
            'id':'password1',
            'required':'required',
        }
    ))

    password2=forms.CharField(label='Contraseña de confirmación',widget=forms.PasswordInput(

        attrs = {
            'class':'form-control',
            'placeholder':'Ingrese nuevamente su contraseña',
            'id':'password2',
            'required':'required',
        }
    ))
    class Meta:
        model=Usuario
        fields={'username','email','nombres','apellidos','dni','salario','admin'}
  
        widgets = {
            
       'username':forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Ingrese su nombre de usuario'
       } ),
       'email':forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'Ingrese sus correo electrónico'
       } ),
       'nombres':forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Ingrese sus nombres'
       } ),
        'apellidos':forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Ingrese sus apellidos'
       } ),
       'dni':forms.NumberInput(attrs={
            'class':'form-control',
            'placeholder':'Ingrese su DNI'
       } ),
       'salario':forms.NumberInput(attrs={
            'class':'form-control',
            'placeholder':'Ingrese su salario'
       } )
       
    }
    admin=forms.BooleanField(initial=False,required=False)


        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2    

    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1']) 
        admin=self.cleaned_data.get('admin')
        if commit:
            user.save()
        if admin == True:
            groups = Group.objects.get(name='Administrador')
            user.groups.add(groups)
        if admin == False:
            group = Group.objects.get(name='Vendedor')
            user.groups.add(group)
        return user
class DateSaleForm(forms.ModelForm):
    class Meta:
        model=DetSale
        fields=['sale','prod','price','cant','subtotal'] 
        sale=forms.ModelChoiceField(queryset=Sale.objects.all())
        prod=forms.ModelChoiceField(queryset=Producto.objects.all())
        ganancia=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese precio'}))
        cant = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese la cantidad'}))
        subtotal=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese subtotal'}))
     
  
class SucursalForm(forms.ModelForm):

    
    class Meta:
        model=Sucursal
        fields=['ciudad','direccion','ganancia']   

    ciudad=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese ciudad de sucursal'}))
    direccion=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese dirección de sucursal'}))
    ganancia=forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese ganancia'}))

class ProductFilter(django_filters.FilterSet):
    nombre=django_filters.CharFilter()
    nombre__gt=django_filters.CharFilter(field_name='nombre', lookup_expr='gt')
    nombre__lt=django_filters.CharFilter(field_name='nombre', lookup_expr='lt')

    class Meta:
        model = Producto
        fields = ['nombre']

class ProveedorForm(forms.ModelForm):

    class Meta:
        model= Proveedor
        
        fields=['nombres','apellidos','ciudad','direccion','telefono','nombreContacto']


    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese el nombre del proveedor'}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese apellidos del proveedor'}))
    ciudad = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Ingrese ciudad del proveedor'}))
    telefono = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese el numero del proveedor'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese la dirección del proveedor'}))

    
class ProductoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Nombre"


    class Meta:
        model= Producto
        
        fields=['nombre','caracteristicas','cantidad','precio','impuestos','descuentoPorc','ubicacionTienda','disponible','sucursal','categoria']


    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese el nombre del producto'}))
    caracteristicas = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Ingrese caracteristicas del producto'}))
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese la cantidad de productos'}))
    precio = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese el precio del producto'}))
    impuestos = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese los impuestos'}))
    descuentoPorc = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Ingrese el descuento ofrecido'}))
    ubicacionTienda = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Ingrese la ubicación de la tienda'}))
    disponible=forms.BooleanField()
    sucursal=forms.ModelChoiceField(queryset=Sucursal.objects.all())
    categoria=forms.ModelChoiceField(queryset=Categoria.objects.all())

    
class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_birthday': DateInput(format='%Y-%m-%d',
                                       attrs={
                                           'value': datetime.now().strftime('%Y-%m-%d'),
                                       }
                                       ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned


class TestForm(Form):
    categories = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    cli = ModelChoiceField(queryset=Client.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))



class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            
                     'cli': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombre',
                }
            ),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
