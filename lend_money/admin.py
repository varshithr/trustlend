from django.contrib import admin
from .models import YourModelName

class YourModelNameAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2', 'field3')  # Customize the fields to display
    search_fields = ('field1', 'field2')  # Customize the fields to search

admin.site.register(YourModelName, YourModelNameAdmin)