from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    
    # fields 
    label = models.CharField(max_length=250)


class TaggedItem(models.Model):

    # fields 
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)

    # Method 1 : creates dependencies 
    # product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    # Method 2 
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()