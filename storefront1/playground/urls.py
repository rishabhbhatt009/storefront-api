from django.urls import path 
from . import views

### URL Config
urlpatterns = [
    path('hello/', views.hello),
    path('database/', views.database),
    path('filter/', views.filter),
    path('orders/', views.orders),
    path('generic_relation/', views.generic_relation),
]