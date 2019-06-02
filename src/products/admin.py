from django.contrib import admin

# Register your models here.
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Good', {'fields': ['name', 'category', 'price']}),
    #     ('Stock details', {'fields': ['quantity' ,'is_service_component']})
    # ]
    fields = (
        ('name', 'slug'),
        'description',
        ('price', 'quantity'),
        ('category', 'is_service_component')
    )

    list_display = ['name', 'category', 'price', 'is_service_component', 'updated']
    list_filter = ['category', 'is_service_component']
    ordering = ['updated']

    search_fields = ['name', 'category']

admin.site.register(Item, ItemAdmin)
