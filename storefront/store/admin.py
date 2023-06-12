from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from django.http.request import HttpRequest
from django.db.models import Count, Value
from . import models

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title'] # collection is __str__ v/s collection_title uses func
    list_select_related = ['collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update']
    ordering = ['title']
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'LOW' if product.inventory < 10 else 'OK'
    
    # another way 
    def collection_title(self, product):
        return product.collection.title


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    list_per_page = 10
    ordering = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id' : str(collection.id)
               }))  
        return format_html('<a href={}>{}</a>', url, collection.product_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (super().get_queryset(request)
                .annotate(product_count = Count('product'))
                )




@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership', 'order_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def order_count(self, customer): 
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer_id' : str(customer.id)                  
               })
               )
        ret = format_html('<a href={}>{} Orders</a>',url,customer.order_count)
        return ret

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (super().get_queryset(request)
                .annotate(order_count = Count('order'))
                )




@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer_name', 'placed_at', 'payment_status']
    list_select_related = ['customer']  
    list_per_page = 10

    def customer_name(self, order):
        return f'{order.customer.first_name}-{order.customer.last_name}'
    
    def product_count(self, product):
        return product.product_count

    # def products(self, order):
    #     order_items = order.orderitem_set.select_related('product')
    #     return ' | '.join(item.product.title for item in order_items)
        
    
    



# admin.site.register(models.Product)
# admin.site.register(models.Collection)