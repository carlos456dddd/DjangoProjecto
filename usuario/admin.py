from django.contrib import admin


from .models import Producto,Categoria,vendedor,Administrador,Sucursal,Usuario,Sale,Client,DetSale,Proveedor



class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    filter_horizontal = ("groups", "user_permissions")

admin.site.register(Usuario,UserAdmin)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(vendedor)
admin.site.register(Administrador)
admin.site.register(Proveedor)
admin.site.register(Sucursal)
admin.site.register(Sale)
admin.site.register(Client)
admin.site.register(DetSale)


