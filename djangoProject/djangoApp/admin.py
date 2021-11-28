from django.contrib import admin
from .models import *
# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    prepopulated_fields={"pass_and_serial": ("pass_serial", "pass_number")}

admin.site.register(VisaType)
admin.site.register(Visa)
admin.site.register(GroupClient)
admin.site.register(Contract)
admin.site.register(Country)
admin.site.register(Client, ClientAdmin)
admin.site.register(Hotel)
admin.site.register(Calls)
