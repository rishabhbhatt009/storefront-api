from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

# URLConf

##################################################################################
# Nested Routers
##################################################################################

# Step 1 : create parent/domain router and register parent resource
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')

# # Step 2 : create child routers and register view
products_router = routers.NestedDefaultRouter(
    parent_router=router, 
    parent_prefix='products', 
    lookup='product'
    ) 

products_router.register(
    prefix='reviews', 
    viewset=views.ReviewViewSet, 
    basename='products-reviews'
)

cart_router = routers.NestedDefaultRouter(
    parent_router=router,
    parent_prefix='carts',
    lookup='cart'
)

cart_router.register(
    prefix='items',
    viewset=views.CartItemViewSet,
    basename='carts-items'
)

urlpatterns = router.urls + products_router.urls + cart_router.urls
# urlpatterns = [
#     path(r'', include(router.urls)),
#     path(r'', include(products_router.urls)),
#     path(r'', include(cart_router.urls))
# ]

##################################################################################
# Routers
##################################################################################

# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)

# urlpatterns = router.urls

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
