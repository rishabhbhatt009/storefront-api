from decimal import Decimal
from rest_framework import serializers
from . models import Product, Collection, Review

###############################################################################
###############################################################################
# 
# There are 2 ways to create a serializer class 
# - Option 1 : 
# - Option 2 : 
# 
###############################################################################
###############################################################################


###############################################################################
### Option 2 : Using model definition to generate serializer
###############################################################################

# -----------------------------------------------------------------------------
# Review Serializer
# -----------------------------------------------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['id', 'product_id','name', 'date', 'description'] 
        read_only_fields = ['product_id']
        
        # product_id = serializers.IntegerField(read_only=True)
        
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
        
# -----------------------------------------------------------------------------
# Product Serializer
# -----------------------------------------------------------------------------

class ProductSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Product
        fields = ['id', 'title', 'slug', 'unit_price', 'inventory', 'collection']
        # fields = ['id', 'title', 'unit_price', 'price', 'price_with_tax', 'collection']
    
    
    ### Custom Fields 
    
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax') 
    collection = serializers.PrimaryKeyRelatedField(queryset = Collection.objects.all())
    # def calculate_tax(self, product : Product):
    #     return round(product.unit_price * Decimal(1.18),2)

# -----------------------------------------------------------------------------
# Collection Serializer 
# -----------------------------------------------------------------------------

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only = True)


###############################################################################
### Option - 1 : Defining each field individually 
###############################################################################

# -----------------------------------------------------------------------------
# Product Serializer
# -----------------------------------------------------------------------------

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255) 
    
#     # fields do not need to match the backend model 
#     # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
#     # new fields can be computed based on functions 
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

#     # ------------------------------------------------------------------------
#     # serializing relations 
#     # ------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Collection Serializer 
# -----------------------------------------------------------------------------

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

#     ### -------------------------------------------------
#     ### Note : this results in multiple queries 
#     ### -------------------------------------------------
#     # product_count  = serializers.SerializerMethodField(method_name='get_product_count')
# 
#     # def get_product_count(self, collection):
#     #     return Product.objects.filter(collection=collection).count()

#     product_count = serializers.IntegerField()

###############################################################################