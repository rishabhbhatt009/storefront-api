from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

# URLConf

##################################################################################
# Routers
##################################################################################

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

# If we have additional custom URLs
# urlpatterns = [
#     # custom urls 
#     path ...
# 
#     path('', include(router.urls)),
# ]
   


##################################################################################
# Class based view urls links 
##################################################################################

# urlpatterns = [   
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:id>/', views.ProductDetails.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetails.as_view()),
# ]

##################################################################################
# Function based view urls links 
##################################################################################

# urlpatterns = [   
#     path('products/', views.product_list),
#     path('products/<int:id>/', views.product_details),
#     path('collections/', views.collection_list, name='collection-list'),
#     path('collections/<int:pk>/', views.collection_details, name='collection-details'),
# ]

##################################################################################
