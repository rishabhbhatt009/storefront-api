from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem


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
# Order and OrderItem Serializers
# -----------------------------------------------------------------------------

class OrderItemProductSerializer(serializers.ModelSerializer):
     class Meta : 
        model = Product
        fields = ['id', 'title', 'unit_price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']
        
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    # OVERWRITE validate : validate input
    def validate_cart_id(self, cart_id):
        
        # check if cart exists
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("Cart does not exist.")
        
        # check if cart is empty 
        if CartItem.objects.filter(cart_id=cart_id).count() == 0 :
            raise serializers.ValidationError("Cart is empty.")
        
        return cart_id
    
    def save(self, **kwargs):
        # print('Cart ID :',self.validated_data['cart_id'])
        # print('User ID :',self.context['user_id'])
        
        # --------------------------------------------------------
        # we want all steps to be atomic 
        # (i.e) all operations should exec or none 
        # --------------------------------------------------------
        with transaction.atomic(): 
            # STEP 1 : get cart id and user id
            user_id = self.context['user_id']
            cart_id = self.validated_data['cart_id']
            
            # STEP 2 : create a new order
            customer, created = Customer.objects.get_or_create(user_id=user_id)
            order = Order.objects.create(customer=customer)
            
            # STEP 3 : get cart items 
            cart_items = (CartItem.objects
                        .select_related('product')
                        .filter(cart_id=cart_id)
                        )
            
            # STEP 4 : create order items from cart items
            order_items = []
            for item in cart_items:
                order_item = OrderItem(order=order, 
                                    product=item.product,
                                    quantity=item.quantity,
                                    unit_price=item.product.unit_price    
                                    )
                order_items.append(order_item)
            OrderItem.objects.bulk_create(order_items)
            
            # STEP 5 : delete cart 
            Cart.objects.filter(pk=cart_id).delete()
        
        return order 
        
# -----------------------------------------------------------------------------
# Customer Profile Serializers
# -----------------------------------------------------------------------------

### If we want additional user information
# class UserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'first_name', 'last_name', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    # user = UserInfoSerializer()
    user_id = serializers.IntegerField(read_only=True) # for testing 
    class Meta : 
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership'] # 'user',

# -----------------------------------------------------------------------------
# Cart and CartItem Serializers
# -----------------------------------------------------------------------------
        
# cart item serializer to display product for cart item
class CartItemProductSerializer(serializers.ModelSerializer):
     class Meta : 
        model = Product
        fields = ['id', 'title', 'unit_price']

# cart item serializer for PUT request
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta : 
        model = CartItem
        fields = ['quantity']

# cart item serializer for POST request         
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    # validating inputs 
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Product does not exist')
        return value 
    
    # you can also set validators in the field definition inside model class 
    # here you get a better error message 
    # def validate_quantity(self,value):
    #     if value <= 0 :
    #         raise serializers.ValidationError('Quantity of product should be at least 1')
    #     return value
    
    # custom saving operation 
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id'] 
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # update existing item 
            print('updating item')
            cart_item.quantity += quantity
            cart_item.save()
            
        except CartItem.DoesNotExist:
            print('new item')
            # create new item 
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        self.instance = cart_item
        return self.instance
        
    class Meta : 
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
    
# cart item serializer for GET request 
class CartItemSerializer(serializers.ModelSerializer):
    
    id  = serializers.IntegerField(read_only=True)
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart_item:CartItem):
        return cart_item.product.unit_price * cart_item.quantity
    
    class Meta : 
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

# cart serializer 
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