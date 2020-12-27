from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from items.models import Item
from smart_selects.db_fields import ChainedForeignKey


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.street_address + ' ' + self.apartment_address

    class Meta:
        verbose_name_plural = ' Addresses'


class Order(models.Model):

    OrderStatus = [
        ('STORE_PICKUP', 'Store Pickup'),
        ('STORE_CANCELLED', 'Store Cancelled'),
        ('ORDERED', 'Ordered'),
        ('CANCELLED', 'Cancelled'),
        ('OUT_FOR_DELIVERY', 'Out for delivery'),
        ('DELIVERED', 'Delivered'),
        ('DECLINED', 'Declined'),
        ('RETURNED', 'Returned'),
        ('REFUND_REQUESTED', 'Refund Requested'),
        ('REFUND_DECLINED', 'Refund Declined'),
        ('REFUND_GRANTED', 'Refund Granted')
    ]

    ModeOfPayment = [
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('COD', 'COD')
    ]

    biller = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT, blank=True, null=True, related_name='biller')
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.PROTECT, blank=True, null=True, related_name='ordered_by')
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(blank=True, null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=10, blank=True)
    store_cancelled_reason = models.CharField(max_length=200, blank=True)
    shipping_address = models.ForeignKey(Address,
                                         on_delete=models.PROTECT, blank=True, null=True)
    order_status = models.CharField(
        max_length=50, choices=OrderStatus, default='STORE_PICKUP')
    refund_reason = models.CharField(max_length=200, blank=True)
    mode_of_payment = models.CharField(
        max_length=50, choices=ModeOfPayment, default='CASH', verbose_name='Payment')
    total = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    def get_order_id(self):
        if self.id is None:
            return '-'
        return self.id

    get_order_id.short_description = 'Order / Invoice ID'

    class Meta:
        verbose_name_plural = ' Orders'

class OrderItemQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.item.available_quantity += obj.quantity
            obj.item.save()
            super(Item, obj.item).save(*args, **kwargs)
        super(OrderItemQuerySet, self).delete(*args, **kwargs)

class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()
    order = models.ForeignKey(Order,
                              on_delete=models.PROTECT)
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name='order_item')
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    item_rate = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_rate = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    instructions = models.CharField(max_length=100, blank=True)
    extra_info = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords()

    def get_item(self):
        return str(self.item.item_name)
    get_item.short_description = 'Item'

    def get_quantity(self):
        return str(self.quantity).rstrip('0').rstrip('.') + ' ' + str(self.item.item_unit.abbreviation)
    get_quantity.short_description = 'Quantity'

    def get_item_rate(self):
        return '₹ ' + str(self.item_rate)+ ' / ' + str(self.item.item_unit.abbreviation)
    get_item_rate.short_description = 'Rate'

    def get_item_rate_receipt(self):
        if self.discounted_rate is None or self.discounted_rate == 0:
            return str(self.item_rate) + ' /' + str(self.item.item_unit.abbreviation)
        return str(self.discounted_rate) + ' /' + str(self.item.item_unit.abbreviation)

    def get_discounted_rate(self):
        if self.discounted_rate is None or self.discounted_rate == 0:
            return '-'
        return '₹ ' + str(self.discounted_rate) + ' /' + str(self.item.item_unit.abbreviation)
    get_discounted_rate.short_description = 'Discounted Rate'

    def get_subtotal(self):
        if self.item_rate is None or self.quantity is None:
            return '-'
        if self.discounted_rate is None or self.discounted_rate == 0:
            return '₹ ' + str(round((self.quantity * self.item_rate), 2))
        else:
            return '₹ ' + str(round((self.quantity * self.discounted_rate), 2))
    get_subtotal.short_description = 'Subtotal'

    def get_subtotal_receipt(self):
        if self.item_rate is None or self.quantity is None:
            return '-'
        if self.discounted_rate is None or self.discounted_rate == 0:
            return str(round((self.quantity * self.item_rate), 2))
        else:
            return str(round((self.quantity * self.discounted_rate), 2))

    def save(self, *args, **kwargs):
        self.item.available_quantity -= self.quantity
        self.item.save()
        # super(Item, self.item).save(*args, **kwargs)
        super(OrderItem, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.item.available_quantity += self.quantity
        self.item.save()
        super(Item, self.item).save(*args, **kwargs)
        super(OrderItem, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Order Items'
