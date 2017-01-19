from django.contrib import admin
from .models import User_Info, User_Star, Restaurant, Restaurant_Info

# Register your models here.

admin.site.register(User_Info, admin.ModelAdmin)
admin.site.register(User_Star, admin.ModelAdmin)
admin.site.register(Restaurant, admin.ModelAdmin)
admin.site.register(Restaurant_Info, admin.ModelAdmin)