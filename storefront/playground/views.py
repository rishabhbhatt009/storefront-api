from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from store.models import Product,Collection, OrderItem

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

    orders = (OrderItem.objects
              .values('product__title', 'product__unit_price')
              .distinct()
              .order_by('product__title')
              )

    return render(request=request,
                  template_name='results.html', 
                  context={
                      'count' : orders.count(),
                      'results' : list(orders)
                      }
                )