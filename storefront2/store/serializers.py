from decimal import Decimal
from rest_framework import serializers
from . models import Product, Collection, Review, Cart, CartItem

###############################################################################
###############################################################################
# 
# There are 2 ways to create a serializer class 
# - Option 1 : Defining each field individually 
# - Option 2 : Using model definition to generate serializer
# 
###############################################################################
###############################################################################


###############################################################################
### Option 2 : Using model definition to generate serializer
###############################################################################

# -----------------------------------------------------------------------------
# Cart and CartItem Serializer
# -----------------------------------------------------------------------------
        
class CartItemProductSerializer(serializers.ModelSerializer):
    
     class Meta : 
        model = Product
        fields = ['id', 'title', 'unit_price']
        
class CartItemSerializer(serializers.ModelSerializer):
    
    id  = serializers.IntegerField(read_only=True)
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.unit_price * cart_item.quantity
    
    class Meta : 
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart:CartItem):
        price_of_each_item = [item.quantity * item.product.unit_price for item in cart.items.all()]
        return sum(price_of_each_item)
    
    class Meta : 
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_price']

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
        fields = ['id', 'title', 'description', 'slug', 'unit_price', 'inventory', 'collection']
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