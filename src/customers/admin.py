from django.contrib import admin
from django.db.models import Count
from django.utils import timezone

from . import models

# Register your models here.
from .models import Profile
from .models import Order
from .models import StockItem

from products.models import Item


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identity', {'fields': ['title', 'last_name', 'first_name' ]}),
        ('Contact details', {'fields': ['email_address' ,'contact_number']}),
        ('Address', {'fields': ['street_address', 'area', 'town']}),
    ]

    list_display = ['admin_name',   'contact_number', 'time_added']
    list_filter = ['area', 'town']
    ordering = ['time_added']

    search_fields = ['first_name', 'last_name', 'area', 'town']

def complete(ModelAdmin, request, queryset):
    queryset.update(
        completed=True,
        completed_at=timezone.now()
    )
complete.short_description = 'Mark orders as complete now'

class StockItemInline(admin.TabularInline):
    model = StockItem
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('item', 'order', 'quantity'),
            )
        }),
    )

class OrderAdmin(admin.ModelAdmin):
    actions = [complete]
    date_hierarchy = 'placed_at'
    inlines = [StockItemInline]
    list_display = ['customer', 'type', 'placed_at', 'completed_at','completed', 'total_cost']
    list_editable = ['completed']
    list_filter = ['completed', 'type', 'placed_at', 'completed_at']
    ordering = ['placed_at']
    readonly_fields = ('placed_at', 'completed_at')

    fieldsets = (
        (None, {
            'fields': (
                ('customer', 'type', 'total_cost', 'completed'),
            )
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': ('placed_at', 'completed_at')
        })
    )

    # filter_horizontal = ['stock_items']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(StockItem)
