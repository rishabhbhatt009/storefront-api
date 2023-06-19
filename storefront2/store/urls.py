from django.urls import path
from . import views

# URLConf
urlpatterns = [
    
    ##################################################################################
    # Function based view urls links 
    ##################################################################################
    
    # path('products/', views.product_list),
    # path('products/<int:id>/', views.product_details),
    # path('collections/', views.collection_list, name='collection-list'),
    # path('collections/<int:pk>/', views.collection_details, name='collection-details'),
    
    ##################################################################################
    # Class based view urls links 
    ##################################################################################
    
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetails.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetails.as_view()),

    ##################################################################################
]
