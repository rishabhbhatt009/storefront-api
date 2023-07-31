from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Collection, Order, OrderItem, Review, Cart, CartItem, Customer
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemProductSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .filters import ProductFilterSet
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission

##############################################################################################
##############################################################################################
# 
# Introduction
#   1. Function based api-views : Own Implementation)
#   2. Class based api-views : Own Implementation
#   3. Generic Views : Inherit the implementation
#   4. Generic ViewSet : Combines multiple views of an endpoint 
#   
##############################################################################################
##############################################################################################

##############################################################################################
# Generic ViewsSet
##############################################################################################

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS-SET for Order and OrderItem 
# ------------------------------------------------------------------------------------------

# Order View
class OrderViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    # OVERWRITE create : return order on creation
    def create(self, request, *args, **kwargs):
        # create order using CreateOrderSerializer 
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
            )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # send created order to OrderSerializer for display 
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    # OVERWRITE get_queryset : different queryset based on permissions
    # queryset = Order.objects.all()
    def get_queryset(self):
        user = self.request.user
        if user.is_staff : 
            return Order.objects.all()
        
        # violates command-query separation principle 
        customer = Customer.objects.get(user_id=user.id)
        return Order.objects.filter(customer_id=customer.id)
 
    
    # OVERWRITE get_serializer_class : different queryset based on request method
    # serializer_class = OrderSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            print('method is patch')
            return UpdateOrderSerializer
        return OrderSerializer
    
    
    # OVERWRITE get_serializer_context : send additional context to serializer
    # Note : no longer required as we are overwriting create 
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}

    # OVERWRITE get_permissions : 
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):     
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
            

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS-SET for User Profile 
# ------------------------------------------------------------------------------------------

# Customer View
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    # defining permission 
    # option 1 : generic (we use class)
    permission_classes = [IsAdminUser]
    
    # option 2 : based on methods (we use objects of classes)
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    
    
    # defining actions 
    
    # we are also overwriting permission_classes
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        
        customer = Customer.objects.get(user_id=request.user.id)
        
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('works')
        
# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS-SET with modification for CART and CART-ITEMS
# ------------------------------------------------------------------------------------------

# Cart ViewSet 
class CartViewSet(CreateModelMixin, 
                  # ListModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin, 
                  GenericViewSet):

    serializer_class = CartSerializer
    
    def get_queryset(self):
        queryset = Cart.objects.prefetch_related('items__product').all()
        return queryset
    
# Cart-Item ViewSet
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    # option 1  : hard coded serializer 
    # serializer_class = CartItemSerializer
    
    # option 2 : dynamically assigning the serializer 
    def get_serializer_class(self):
        if self.request.method == 'POST': 
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        queryset = (CartItem.objects
                    .filter(cart_id=self.kwargs['cart_pk'])
                    # ------------------------------------------------------------------------
                    # Note : this is a good place to notice the difference b/w 
                    # 1. prefetch related : generates a single query where "item IN (...)" 
                    # 2. select related : generates a query with an inner join for more info.
                    # ------------------------------------------------------------------------
                    # .prefetch_related('product')
                    .select_related('product')
                    )
        return queryset

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS-SET for reviews 
# ------------------------------------------------------------------------------------------

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        # queryset = Review.objects.all()
        queryset = Review.objects.filter(product_id=self.kwargs['product_pk'])
        return queryset
    
    # send product_id to serializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS-SET for product-endpoint 
# ------------------------------------------------------------------------------------------

class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    ### Adding Permissions 
    permission_classes = [IsAdminOrReadOnly]
    
    ### Adding Pagination 
    pagination_class = DefaultPagination
    
    # ------------------------------------------------ 
    # Adding generic filtering 
    # ------------------------------------------------
    
    ### simple generic filters 
    # filter_backends = [DjangoFilterBackend] 
    # filterset_fields = ['collection_id', 'unit_price']
    
    ### custom generic filters 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
    filterset_class = ProductFilterSet
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'inventory']
    
    # ------------------------------------------------ 
    # Adding simple filtering from URL params
    # ------------------------------------------------
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()        
    #     collection_id = self.request.query_params.get('collection_id', None)
        
    #     # Adding filter if query parameter exists
    #     if collection_id :
    #         queryset = queryset.filter(collection_id = collection_id)
            
    #     return queryset
    # ------------------------------------------------
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        order_items = OrderItem.objects.filter(product_id=kwargs['pk']).count() 
        if order_items > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # SHOULDN'T USE DELETE : use destroy instead 
    # 
    # def delete(self, request:Request, pk) -> Response :
    #     product = get_object_or_404(Product,pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS-SET for collection-endpoint 
# ------------------------------------------------------------------------------------------

class CollectionViewSet(ModelViewSet):
    
    queryset = (Collection.objects
                .annotate(products_count = Count('products'))
                .all())
    serializer_class = CollectionSerializer
    
    # adding permissions 
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        product_count = Product.objects.select_related('collection').filter(collection_id = kwargs['pk']).count()
        if product_count > 0:
            return Response({'error': f'Collection cannot be deleted because it includes one or more products ({product_count}).'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    
##############################################################################################
# GENERIC VIEWS
##############################################################################################

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS for product-list 
# ------------------------------------------------------------------------------------------

# class ProductList(ListCreateAPIView):

#     # Attributes ----------------------------------------------------------------------------
#     queryset = Product.objects.select_related('collection').all()[:10]
#     serializer_class = ProductSerializer
    
#     # Functions ----------------------------------------------------------------------------
    
#     # def get_queryset(self):
#     #     queryset = Product.objects.select_related('collection').all()[:10]
#     #     # add logic here 
#     #     return queryset
    
#     # def get_serializer(self, *args, **kwargs):
#     #     # add logic here 
#     #     return ProductSerializer
    
#     # ---------------------------------------------------------------------------------------
    
#     def get_serializer_context(self):
#         return {'request': self.request}

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS for product-details 
# ------------------------------------------------------------------------------------------

# class ProductDetails(RetrieveUpdateDestroyAPIView):
    
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self, request:Request, pk) -> Response :
#         product = get_object_or_404(Product,pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS for collection-list 
# ------------------------------------------------------------------------------------------

# class CollectionList(ListCreateAPIView):

#     queryset = (Collection.objects
#                 .annotate(products_count = Count('products'))
#                 .all()
#                 )
#     serializer_class = CollectionSerializer

# ------------------------------------------------------------------------------------------
# Using GENERIC VIEWS for collection-details 
# ------------------------------------------------------------------------------------------

# class CollectionDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count = Count('products'))
#     serializer_class = CollectionSerializer
    
#     def delete(self, request:Request, pk) -> Response : 
#         collection = get_object_or_404(Collection,pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response({'MF WAS DELETED'}, status=status.HTTP_204_NO_CONTENT)
    

##############################################################################################
# Class Based Views :
##############################################################################################

# --------------------------------------------------------------------------------------------
# Class based API-View for product list 
# --------------------------------------------------------------------------------------------

# class ProductList(APIView):
    
#     def get(self, request:Request) -> Response : 
#         queryset = Product.objects.select_related('collection').all()[:10]
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request:Request) -> Response :
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True) # replacement for if(valid)``
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)    

    
# --------------------------------------------------------------------------------------------
# Class based API-View for product details
# --------------------------------------------------------------------------------------------

# class ProductDetails(APIView):    
    
#     def get(self, request:Request, id) -> Response : 
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)    
        
#     def post(self, request:Request, id) -> Response :
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
                
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)    
    
#     def delete(self, request:Request, id) -> Response :
#         product = get_object_or_404(Product,pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        

# --------------------------------------------------------------------------------------------
# Class based API View for collection list 
# --------------------------------------------------------------------------------------------
     
# @api_view(['GET','POST'])
# def collection_list(request: Request):
    
#     if request.method == 'GET' : 
#         queryset = (Collection.objects
#                        .annotate(products_count = Count('products'))
#                        .all()
#                        )
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)  
        
#     elif request.method == 'POST' :
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


##############################################################################################
# Function Based Views :
##############################################################################################

# --------------------------------------------------------------------------------------------
# Function based API-View for product list 
# --------------------------------------------------------------------------------------------

# @api_view(['GET', 'POST'])
# def product_list(request):

#     if request.method == 'GET': 
#         queryset = Product.objects.select_related('collection').all()[:10]
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)

#         ### replacement for if(valid)``
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('Gotha')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# --------------------------------------------------------------------------------------------
# Function based API-View for product details
# - the end point supports get, put and delete request 
# --------------------------------------------------------------------------------------------

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details(request, id):

#     # try : 
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
    
#     # except Product.DoesNotExist : 
#     #     return Response(status=status.HTTP_404_NOT_FOUND) 

#     product = get_object_or_404(Product,pk=id)
    
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)    
    
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
                
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)    
    
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------------------------------------------------------------------
# API View for product list 
# --------------------------------------------------------------------------------------------
    
# @api_view(['GET', 'POST', 'DELETE'])
# def collection_details(request:Request, pk):
#     query_set = Collection.objects.annotate(products_count = Count('products'))
#     collection = get_object_or_404(query_set,pk=pk)
    
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)    
    
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response({'MF WAS DELETED'}, status=status.HTTP_204_NO_CONTENT)
    
# --------------------------------------------------------------------------------------------
# Function based API View for collection list 
# --------------------------------------------------------------------------------------------
     
# @api_view(['GET','POST'])
# def collection_list(request: Request):
    
#     if request.method == 'GET' : 
#         queryset = (Collection.objects
#                        .annotate(products_count = Count('products'))
#                        .all()
#                        )
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)  
        
#     elif request.method == 'POST' :
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

##############################################################################################