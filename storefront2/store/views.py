from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

##############################################################################################
# Class Based Views :
##############################################################################################

# --------------------------------------------------------------------------------------------
# Class based API-View for product list 
# --------------------------------------------------------------------------------------------

class ProductList(APIView):
    
    def get(self, request:Request) -> Response : 
        queryset = Product.objects.select_related('collection').all()[:10]
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request:Request) -> Response :
        serializer = ProductSerializer(data=request.data)
        ### replacement for if(valid)``
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)    

# --------------------------------------------------------------------------------------------
# Class based API-View for product details
# --------------------------------------------------------------------------------------------

class ProductDetails(APIView):    
    
    def get(self, request:Request, id) -> Response : 
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)    
        
    def post(self, request:Request, id) -> Response :
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
                
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)    
    
    def delete(self, request:Request, id) -> Response :
        product = get_object_or_404(Product,pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

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
     

@api_view(['GET','POST'])
def collection_list(request: Request):
    
    if request.method == 'GET' : 
        collections = (Collection.objects
                       .annotate(products_count = Count('products'))
                       .all()
                       )
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)  
        
    elif request.method == 'POST' :
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# --------------------------------------------------------------------------------------------
# API View for product list 
# --------------------------------------------------------------------------------------------
    
@api_view(['GET', 'POST', 'DELETE'])
def collection_details(request:Request, pk):
    query_set = Collection.objects.annotate(products_count = Count('products'))
    collection = get_object_or_404(query_set,pk=pk)
    
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)    
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({'MF WAS DELETED'}, status=status.HTTP_204_NO_CONTENT)
    
##############################################################################################