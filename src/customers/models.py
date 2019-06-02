from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from products.models import Item


class Profile(models.Model):
    MR = 'MR'
    MRS = 'MRS'
    MS = 'MS'
    TITLE = (
        (MR, 'Mr.'),
        (MRS, 'Mrs.'),
        (MS, 'Ms.')
    )
    title = models.CharField(max_length=4, choices=TITLE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street_address = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    email_address = models.CharField(max_length=30, blank=True)
    time_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f' {self.first_name} {self.last_name} ({self.email_address})'

    @property
    def admin_name(self):
        return f' {self.first_name} {self.last_name} ({self.email_address})'

    # admin_name.short_description = 'customer'

class Order(models.Model):
    PURCHASE = 'PURCHASE'
    RENTAL = 'RENTAL'
    TYPE = (
        (PURCHASE, 'purchase'),
        (RENTAL, 'rental')
    )
    customer = models.ForeignKey(Profile, related_name='order', on_delete=models.CASCADE)
    stock_items = models.ManyToManyField('products.Item', blank=True, through='StockItem')
    type = models.CharField(max_length=8, choices=TYPE)
    total_cost = models.DecimalField('total', max_digits=9, decimal_places=2)
    completed = models.BooleanField(default=False)
    placed_at = models.DateTimeField('placed', default=timezone.now)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f' {self.customer} {self.type}'

def post_save_order_create(sender, instance, created, *args, **kwargs):
    if created:
        order.objects.get_or_create(customer=instance)

    order, created = order.objects.get_or_create(customer=instance)

    if order.stock_item is None or order.stock_item == '':
        new_order_stock_item = order.stock_item.create(stock_item=instance.stock_item)
        order.stock_item = new_order_stock_item['id']
        order.save()

post_save.connect(post_save_order_create, sender=Item)


class StockItem(models.Model):
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    # price = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f' {self.item}, {self.order}'
