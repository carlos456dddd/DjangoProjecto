"""puntoventa1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from usuario.views import Inicio
from usuario.views import listarProducto,listarSucursal,listarUsuario,TestView, ListaSale,ListaPdf,SaleListView,listarProveedor,listarDetallesSale





urlpatterns = [
    path('admin/', admin.site.urls),
    path('listar_producto/',login_required(listarProducto.as_view()),name='listar_producto'),
    path('listar_sucursal/',login_required(listarSucursal.as_view()),name='listar_sucursal'),
    path('listar_detalles/',login_required(listarDetallesSale.as_view()),name='listar_detalles'),
    path('listar_usuario/',login_required(listarUsuario.as_view()),name='listar_usuario'),
    path('listar_proveedor/',login_required(listarProveedor.as_view()),name='listar_proveedor'),
    path('listar_vendedor/',login_required(SaleListView.as_view()),name='listar_vendedor'),
    path('listar_sale/',login_required( ListaSale.as_view()),name='listar_sale'),
path('vendedor/', TestView.as_view(), name='vendedor'),
path('listar_pdf/',login_required( ListaPdf.as_view()),name='listar_pdf'),
    path('usuario/',include(('usuario.urls','usuario'))),
    path('inicio/',Inicio.as_view(),name='index'),   
    
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True, 
        template_name='registration/login.html',
        ), 
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
        ), 
        name='logout'
    ),
    
]
