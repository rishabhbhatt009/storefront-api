from decimal import Decimal
from rest_framework import serializers
from . models import Product, Collection

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


### Option - 1 : Defining each field individually 
### -------------------------------------------------
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255) 
    
#     # fields do not need to match the backend model 
#     # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
#     # new fields can be computed based on functions 
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#     # serializing relations 
#     # Option 1: collection = serializers.PrimaryKeyRelatedField(queryset = Collection.objects.all())
#     # Option 2: collection = serializers.StringRelatedField()
#     # Option 3: collection = CollectionSerializer()
#     # Option 4:
#     collection = serializers.HyperlinkedRelatedField(
#         queryset = Collection.objects.all(),
#         view_name= 'collection-details'
#     )


#     def calculate_tax(self, product : Product):
#         return round(product.unit_price * Decimal(1.18),2)


### Option 2 : Using model definition to generate serializer
# -------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Product
        fields = ['id', 'title', 'unit_price']
        # fields = ['id', 'title', 'unit_price', 'price', 'price_with_tax', 'collection']
    
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax') 
    # collection = CollectionSerializer()
    
    def calculate_tax(self, product : Product):
        return round(product.unit_price * Decimal(1.18),2)
