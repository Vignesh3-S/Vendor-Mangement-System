from django.contrib import admin
from .models import Vendor,Purchase_Order,Historical_Performance

admin.site.register(Vendor)
admin.site.register(Purchase_Order)
admin.site.register(Historical_Performance)

# Register your models here.
