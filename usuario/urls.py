from django.urls import path

from django.contrib.auth.decorators import login_required
from .views import crearProducto
from .views import listarProducto,ActualizarProducto,crearProducto,borrarProducto
from .views import listarSucursal,ActualizarSucursal,crearSucursal,borrarSucursal
from .views import listarUsuario,crearUsuario,ActualizarUsuario,borrarUsuario
from .views import listarUsuarioVendedor,TestView, ListaSale,ListaPdf,SaleListView
from .views import listarProveedor,ActualizarProveedor,crearProveedor,borrarProveedor
from .views import listarDetallesSale,ActualizarDetallesSale,borrarDetallesSale,SaleActualizar,borrarSale

from .views import product_list
from . import views
urlpatterns=[
path('crear_producto/',login_required(crearProducto.as_view()),name='crear_producto'),
path('listar_producto/',login_required(listarProducto.as_view()),name='listar_producto'),
path('editar_producto/<int:pk>',login_required(ActualizarProducto.as_view()),name='editar_producto'),
path('eliminar_producto/<int:pk>',login_required(borrarProducto.as_view()),name='eliminar_producto'),


path('list/', product_list, name="product-list"),
path('crear_sucursal/',login_required(crearSucursal.as_view()),name='crear_sucursal'),
path('listar_sucursal/',login_required(listarSucursal.as_view()),name='listar_sucursal'),
path('editar_sucursal/<int:pk>',login_required(ActualizarSucursal.as_view()),name='editar_sucursal'),
path('eliminar_sucursal/<int:pk>',login_required(borrarSucursal.as_view()),name='eliminar_sucursal'),

path('crear_proveedor/',login_required(crearProveedor.as_view()),name='crear_proveedor'),
path('listar_proveedor/',login_required(listarProveedor.as_view()),name='listar_proveedor'),
path('editar_proveedor/<int:pk>',login_required(ActualizarProveedor.as_view()),name='editar_proveedor'),
path('eliminar_proveedor/<int:pk>',login_required(borrarProveedor.as_view()),name='eliminar_proveedor'),


path('listar_detalles/',login_required(listarDetallesSale.as_view()),name='listar_proveedor'),
path('editar_detalles/<int:pk>',login_required(ActualizarDetallesSale.as_view()),name='editar_detalles'),
path('eliminar_detalles/<int:pk>',login_required(borrarDetallesSale.as_view()),name='eliminar_detalles'),


path('editar_sale/<int:pk>',login_required(SaleActualizar.as_view()),name='editar_sale'),
path('borrar_sale/<int:pk>',login_required(borrarSale.as_view()),name='borrar_sale'),



path('crear_usuario/',login_required(crearUsuario.as_view()),name='crear_usuario'),
path('listar_usuario/',login_required(listarUsuario.as_view()),name='listar_usuario'),
path('editar_usuario/<int:pk>',login_required(ActualizarUsuario.as_view()),name='editar_usuario'),
path('eliminar_usuario/<int:pk>',login_required(borrarUsuario.as_view()),name='eliminar_usuario'),
path('listar_vendedor', SaleListView.as_view(), name='listar_vendedor'),
path('vendedor/', TestView.as_view(), name='vendedor'),
path('listar_usuario_vendedor/',login_required(listarUsuarioVendedor.as_view()),name='listar_usuario_vendedor'),
path('listar_sale/',login_required( ListaSale.as_view()),name='listar_sale'),
path('listar_pdf/', views.ListaPdf.as_view(),name='listar_pdf')

]
