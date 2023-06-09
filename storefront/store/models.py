from django.db import models

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=250)
    discount = models.FloatField()


class Collection(models.Model):

    # fields 
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(to='Product', on_delete=models.SET_NULL, null=True, related_name='+')
    

class Product(models.Model):    

    # fields
    title = models.CharField(max_length=250)
    slug = models.SlugField(default='-')
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)

    # relationships
    collection = models.ForeignKey(to=Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(to=Promotion)
    

class Customer(models.Model):
    
    MEMBERSHIP_DEFAULT = 'STD'
    
    MEMBERSHIP_CHOICES = [
        ('GLD', 'GOLD'),
        ('SIL', 'SILVER'),
        ('STD', 'STANDARD')
    ] 
    
    # fields
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=3, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_DEFAULT)

    # # metadata
    # class Meta : 
    #     db_table = 'store_front'
    #     indexes = [models.Index(fields=['last_name', 'first_name'])]

class Order(models.Model):
    
    PAYMENT_DEFAULT = 'P'
    
    PAYMENT_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed')
    ]

    # fields
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_DEFAULT)
    
    # relationships
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT)
    # item = models.ForeignKey(to='OrderItem', on_delete=models.PROTECT) ### never be deleted since we should preserve sales


class OrderItem(models.Model):
   
    # filed 
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # relationships 
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    

class Address(models.Model):
    '''
    1-1 relationship between customer and address
    Customer(parent) <--- Address(child)
    
    '''
    # fields
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250) 
    
    # relationships 
    # customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    
    # fields
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):

    # filed 
    quantity = models.PositiveSmallIntegerField()

    # relationships 
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)