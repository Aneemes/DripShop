from django.contrib import admin
from .models import Brand

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

admin.site.register(Brand, BrandAdmin)