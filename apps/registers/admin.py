from django.contrib import admin
from .models import FuelStorage, RegisterFuel, FuelStorageLocal, FuelStorageExtern


admin.site.register(FuelStorage)
admin.site.register(RegisterFuel)
admin.site.register(FuelStorageLocal)
admin.site.register(FuelStorageExtern)
