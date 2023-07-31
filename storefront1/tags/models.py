from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

# custom manager class
class CustomManager_Tags(models.Manager):

    def get_tags(self, object_type, object_id): 

        content_type_id = ContentType.objects.get_for_model(object_type)
        tags = (TaggedItem.objects
                .select_related('tag')
                .filter(
                        content_type = content_type_id,
                        object_id = object_id
                    )
                )
        return tags 


class Tag(models.Model):
    
    # fields 
    label = models.CharField(max_length=250)


class TaggedItem(models.Model):

    # for custom manager 
    objects = CustomManager_Tags()
    
    # fields 
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)

    # Method 1 : creates dependencies 
    # product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    # Method 2 
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()