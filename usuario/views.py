from django.shortcuts import render,redirect
from .forms import ProductoForm,SucursalForm,FormularioUsuario,ProductFilter,TestForm,SaleForm,ClientForm,ProveedorForm,DateSaleForm
from .models import Producto,Sucursal,Categoria,Sale,Client,DetSale,Proveedor
from .models import Usuario
from django.http import HttpResponse
import json
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView,View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .util import render_to_pdf



class listarProveedor(ListView):  
    
    redirect_field_name='login'
    model=Proveedor
    template_name = 'proveedor/listar_proveedor.html'
    context_object_name='proveedores'
    queryset=Proveedor.objects.all()

class ActualizarProveedor(UpdateView):
    model=Proveedor
    form_class=ProveedorForm
    template_name='proveedor/proveedor.html'
    success_url=reverse_lazy('usuario:listar_proveedor')

    
class crearProveedor(CreateView):
    model=Proveedor
    form_class=ProveedorForm
    template_name='proveedor/crear_proveedor.html'
    success_url=reverse_lazy('usuario:listar_proveedor')

class borrarProveedor(DeleteView):
    model=Proveedor
    form_class=ProveedorForm
    template_name='proveedor/proveedor_confirm_delete.html'
    success_url=reverse_lazy('usuario:listar_proveedor')



class listarDetallesSale(ListView):  
    
    redirect_field_name='login'
    model=DetSale
    template_name = 'detalles/listar_detalles.html'
    context_object_name='detalles'
    queryset=DetSale.objects.all()

class ActualizarDetallesSale(UpdateView):
    model=DetSale
    form_class=DateSaleForm
    template_name='detalles/detalles.html'
    success_url=reverse_lazy('usuario:listar_detalles')


class borrarDetallesSale(DeleteView):
    model=DetSale
    form_class=DateSaleForm
    template_name='detalles/detsale_confirm_delete.html'
    success_url=reverse_lazy('usuario:listar_detalles')









class SaleActualizar(UpdateView):
    model=Sale
    template_name='sale/sale.html'
    form_class=SaleForm
    success_url=reverse_lazy('usuario:listar_sale')
class borrarSale(DeleteView):
    model=Sale
    form_class=SaleForm
    template_name='sale/sale_confirm_delete.html'
    success_url=reverse_lazy('usuario:listar_sale')


class SaleListView(ListView):
    model = Sale
    template_name = 'usuarioRegistro/lista_vendedor.html'
 

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('usuario:vendedor')
        context['list_url'] = reverse_lazy('erp:lista_vendedor')
        context['entity'] = 'Ventas'
        return context

class TestView(TemplateView):
    template_name = 'usuarioRegistro/vendedor.html'



    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
   
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]:
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre

                    data.append(item)  
            elif action == 'search_data':
                data = []
                clien=Client.objects.filter(names__icontains=request.POST['term'])[0:10]
                for i in clien:
                    item=i.toJSON()
                    item['value']=i.names
                    data.append(item)
            elif action =='add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['idProducto']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                          
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()
        producto = Producto.objects.all()
        sale=Sale.objects.all()
        context={'categorias': categorias, 'producto': producto,'sale':sale}        
        context['title'] = 'Select Aninados | Django'
        context['action'] = 'add'
        context['form'] = TestForm()
        return context       
class ListaPdf(View):
    def get(self,request,*args,**kwargs):
        ventas=Sale.objects.all()
        data={'ventas':ventas}

        pdf = render_to_pdf('sale/imprimir.html',data)

        return HttpResponse(pdf, content_type='application/pdf')


        
class ListaSale(ListView):
    redirect_field_name='login'
    model=Sale
    template_name = 'sale/listar_sale.html'
    context_object_name='sale'
    queryset=Sale.objects.all()


class Inicio(TemplateView): 
    template_name='index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated==True:
            group_name = request.user.groups.all()[0].name

        if group_name == "Administrador":
            return render(request,'index.html')

        elif group_name == "Vendedor":
            return redirect('vendedor')
        
        else:
            return redirect('index')

#  Producto modelo mostrar#
          
class listarProducto(ListView):  
    
    redirect_field_name='login'
    model=Producto
    template_name = 'usuario/listar_producto.html'
    context_object_name='productos'
    queryset=Producto.objects.all()

class ActualizarProducto(UpdateView):
    model=Producto
    form_class=ProductoForm
    template_name='usuario/producto.html'
    success_url=reverse_lazy('usuario:listar_producto')

    
class crearProducto(CreateView):
    model=Producto
    form_class=ProductoForm
    template_name='usuario/crear_producto.html'
    success_url=reverse_lazy('usuario:listar_producto')

class borrarProducto(DeleteView):
    model=Producto
    form_class=ProductoForm
    template_name='usuario/producto_confirm_delete.html'
    success_url=reverse_lazy('usuario:listar_producto')

#Sucursal-/()
class listarSucursal(ListView):  
    redirect_field_name='login'
    model=Sucursal
    template_name ='sucursal/listar_sucursal.html'
    context_object_name='sucursales'
    queryset=Sucursal.objects.all()

class ActualizarSucursal(UpdateView):
    model=Sucursal
    form_class=SucursalForm
    template_name='sucursal/sucursal.html'
    success_url=reverse_lazy('usuario:listar_sucursal')

    
class crearSucursal(CreateView):
    model=Sucursal
    form_class=SucursalForm
    template_name='sucursal/crear_sucursal.html'
    success_url=reverse_lazy('usuario:listar_sucursal')

class borrarSucursal(DeleteView):
    model=Sucursal
    form_class=SucursalForm
    template_name='sucursal/sucursal_confirm_delete.html'
    success_url=reverse_lazy('usuario:listar_sucursal')

#Usuario

def product_list(request):
    f = ProductFilter(request.GET, queryset=Producto.objects.all())
    return render(request, 'my_app/template.html', {'filter': f})

class crearUsuario(CreateView):
    model=Usuario
    form_class=FormularioUsuario
    template_name='usuarioIngreso/crear_usuario.html'
    success_url=reverse_lazy('usuario:listar_usuario')


class listarUsuario(ListView):
    redirect_field_name='login'
    model=Usuario
    template_name='usuarioIngreso/listar_usuario.html'
    queryset=Usuario.objects.all()


class ActualizarUsuario(UpdateView):
    model=Usuario
    form_class=FormularioUsuario
    template_name='usuarioIngreso/usuario.html'
    success_url=reverse_lazy('usuario:listar_usuario')

class borrarUsuario(DeleteView):
    model=Usuario
    form_class=FormularioUsuario
    template_name='usuarioIngreso/usuario_confirm_delete.html'
    success_url=reverse_lazy('usuario:listar_usuario')






#Visalizar tabla de productossdsd

class listarUsuarioVendedor(ListView):
    redirect_field_name='login'
    model=Producto
    template_name='usuarioRegistro/listar_producto for vendedor.html'
    queryset=Producto.objects.all()




#Visualizar listas de categorías

class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'usuarioRegistro/vendedor.html'
  

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(name__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context










  
