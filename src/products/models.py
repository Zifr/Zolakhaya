from django.db import models
from django.db.models.signals import pre_save

from .utils import unique_slug_generator


class Item(models.Model):
    EQUIPMENT = 'EQUIPMENT'
    POULTRY = 'POULTRY'
    PRODUCE = 'PRODUCE'
    PROTEIN = 'PROTEIN'
    NONE = 'NA'
    PRODUCT_TYPE_CHOICES = (
        (EQUIPMENT, 'Equipment'),
        (POULTRY, 'Poultry'),
        (PRODUCE, 'Produce'),
        (PROTEIN, 'Protein'),
        (NONE, 'None'),
    )
    name = models.CharField('product', max_length=70)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default=NONE)
    is_service_component = models.BooleanField('service component', default=False)
    time_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

def pi_pre_save_receiver(sender, instance, *args, **kwargs):
    print('saving..')
    print(instance.category)
    print(instance.time_added)
    print(instance.slug)
    if not instance.slug:
      instance.slug = unique_slug_generator(instance)


pre_save.connect(pi_pre_save_receiver, sender=Item)
