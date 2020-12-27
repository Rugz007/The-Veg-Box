from django.db import models
from django.utils.timezone import now
from simple_history.models import HistoricalRecords
from items.models import Item


class Vendor(models.Model):
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class PurchaseOrder(models.Model):

    ModeOfPayment = [
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card')
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    date = models.DateField()
    total = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    mode_of_payment = models.CharField(
        max_length=50, choices=ModeOfPayment, default='CASH', verbose_name='Payment')
    paid = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = '   Purchase Orders'


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    expected_error = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, verbose_name='Expected Quantity Error')
    cost_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    history = HistoricalRecords()

    def get_item(self):
        return str(self.item.item_name)
    get_item.short_description = 'Item'

    def get_quantity(self):
        return str(self.quantity) + ' ' + str(self.item.item_unit.abbreviation)
    get_quantity.short_description = 'Quantity'

    def get_expected_error(self):
        return str(self.quantity) + ' ' + str(self.item.item_unit.abbreviation)
    get_expected_error.short_description = 'Expected Quantity Error'

    def get_cost_price(self):
        return '₹ ' + str(self.cost_price) + ' / ' + str(self.item.item_unit.abbreviation)
    get_cost_price.short_description = 'Cost Price'

    def get_subtotal(self):
        if self.cost_price is None or self.quantity is None or self.cost_price == 0:
            return '-'
        else:
            return '₹ ' + str(round((self.quantity * self.cost_price), 2))
    get_subtotal.short_description = 'Subtotal'

    def save(self, *args, **kwargs):
        self.item.available_quantity += self.quantity
        if self.item.purchase_price_multiplier != 0:
            self.item.rate = self.item.purchase_price_multiplier * self.cost_price
        self.item.save()
        super(Item, self.item).save(*args, **kwargs)
        super(PurchaseOrderItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.item.available_quantity -= self.quantity
        self.item.save()
        super(Item, self.item).save(*args, **kwargs)
        super(PurchaseOrderItem, self).delete(*args, **kwargs)

    def item_name(self):
        return str(self.item.item_name)
    
    class Meta:
        verbose_name_plural = '  Purchase Order Items'
