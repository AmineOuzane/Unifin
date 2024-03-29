from django.contrib import admin
from .models import Produit,Category,Order,Cart


# Register your models here.
admin.site.register(Produit)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)