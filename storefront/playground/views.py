from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from store.models import Product,Collection, OrderItem, Order
from tags.models import TaggedItem

import random
# Create your views here.

def hello(request):
    # return HttpResponse('Hello World')
    return render(request=request,
                  template_name='hello.html',
                  context={'name' : 'Rishabh', 'emotion':'happy'}
                  )

def database(request):

    count = Product.objects.count()
    products = Product.objects.all()
    sample = Product.objects.get(id=random.randint(1,count))
    collections = Collection.objects.all()

    res = products.filter(id__gt=22)

    return render(request=request,
                  template_name='showcase.html',
                  context={
                      'name' : 'Rishabh', 
                      'count':count, 
                      'sample':sample,
                      'products':products[:10],
                      'collections':collections[:5],
                      }
                  )

def filter(request):
    
    res1 = Product.objects.filter(unit_price__lt=20)
    res2 = Product.objects.filter(collection__title='Cleaning')
    
    return render(request=request,
                  template_name='showcase.html',
                  context={
                      'name' : 'Rishabh', 
                      'count': '<>', 
                      'sample': '<>',
                      'products': res1[:10],
                      'collections':res2[:10],
                      }
                )

def orders(request):

    # orderitems with product name and price 
    # orders = (OrderItem.objects
    #           .values('product__title', 'product__unit_price')
    #           .distinct()
    #           .order_by('product__title')
    #           )

    # orders with product name, price and collection title
    
    # orderitems with product name, price and collection name
    # ordered_products = (OrderItem.objects
    #                     .values('product_id')
    #                     .distinct()
    #                     )
    
    # products = (Product.objects
    #             .filter(id__in=ordered_products)
    #             .values('title', 'unit_price', 'collection__title')
    #             .order_by('-unit_price')
    #             )    

    # last 5 order
    orders = (OrderItem.objects
              .select_related('order', 'product')
              .select_related('order__customer')
              .values('order__id', 'order__placed_at',
                      'quantity','unit_price',
                      'product__title',
                      'order__customer__email'
                      )
              .order_by('-order__placed_at')
              )[:5]
 
    return render(request=request,
                  template_name='results.html', 
                  context={
                      'count' : 0,
                      'results' : list(orders)
                      }
                )

def generic_relation(request):

    product_id = 1
    res = list(TaggedItem.objects.get_tags(Product,product_id))

    return render(request=request,
                template_name='hello.html',
                context={'name' : 'Rishabh', 'emotion':'happy'}
                )
