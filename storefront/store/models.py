from django.db import models

# Create your models here.

### Entities

# Entity 
class Product(models.Model):
    
    # fields
    # Docs : https://docs.djangoproject.com/en/4.2/ref/models/fields/#model-field-types 
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    
### Entity  
class Collection(models.Model):

    # fields 
    title = models.CharField(max_length=255)
    # relationships
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)

# Entity
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

    # relationships
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE)

# Entity 
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
    item = models.ForeignKey(to='OrderItem', on_delete=models.PROTECT) ### never be deleted since we should preserve sales


### Entity
class Address(models.Model):
    '''
    1-1 relationship between customer and address
    Customer(parent) ---> Address(child)
    
    '''
    # fields
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250) 
    # relationships 
    customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, primary_key=True)

### Entity  
class Cart(models.Model):

    # fields
    created_at = models.DateTimeField(auto_now_add=True)
    item_count = models.AutoField()
    # relationships 
    item = models.ForeignKey(to='CartItem', on_delete=models.CASCADE)    

### Entity 
class OrderItem(models.Model):
    # filed 
    
    # relationships 
    pass

### Entity 
class CartItem(models.Model):
    # filed 

    # relationships 
    pass

