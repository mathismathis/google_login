from django.contrib import admin
from myapp.models import User

class YourModelNameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

admin.site.register(User, YourModelNameAdmin)