from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from items.models import Item

class Discard(models.Model):

    discarder = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.PROTECT, blank=True, null=True, related_name='discarder')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    def get_discard_id(self):
        if self.id is None:
            return '-'
        return self.id

    get_discard_id.short_description = 'Discard ID'

    class Meta:
        verbose_name_plural = ' Discards'


class DiscardItem(models.Model):

    ReasonsForDiscard = [
        ('DOA', 'DOA'),
        ('SPOILT', 'Spoilt'),
        ('DAMAGED', 'Damaged'),
        ('RETURNED', 'Returned'),
        ('UNSOLD', 'Unsold')
    ]

    discard = models.ForeignKey(Discard,
                              on_delete=models.PROTECT)
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name='discard_item')
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    item_purchase_rate = models.DecimalField(max_digits=8, decimal_places=2)
    reason = models.CharField(
        max_length=50, choices=ReasonsForDiscard, default='DOA')
    extra_info = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords()

    def get_item(self):
        return str(self.item).split()[0]
    get_item.short_description = 'Item'

    def get_quantity(self):
        return str(self.quantity) + ' ' + str(self.item).split()[5]
    get_quantity.short_description = 'Quantity'

    def get_item_purchase_rate(self):
        return '₹ ' + str(self.item_purchase_rate) + ' ' + str(self.item).split()[4] + ' ' + str(self.item).split()[5]
    get_item_purchase_rate.short_description = 'Purchase Rate'

    def get_subtotal(self):
        if self.item_purchase_rate is None or self.quantity is None:
            return '-'
        else:
            return '₹ ' + str(round((self.quantity * self.item_purchase_rate), 2))
    get_subtotal.short_description = 'Subtotal'

    def save(self, *args, **kwargs):
        self.item.available_quantity -= self.quantity
        self.item.save()
        super(Item, self.item).save(*args, **kwargs)
        super(DiscardItem, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Discarded Items'
