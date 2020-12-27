from django.db import models
from django.utils.timezone import now
from simple_history.models import HistoricalRecords
from units.models import Unit
from smart_selects.db_fields import ChainedForeignKey


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.CharField(max_length=50)

    def __str__(self):
        return self.subcategory
    
    class Meta:
        verbose_name_plural = 'Sub-Categories'


class Item(models.Model):
    item_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field='category',
        chained_model_field='category',
        show_all=False,
        auto_choose=True,
        on_delete=models.PROTECT,
        sort=True)
    item_unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT, related_name='item_unit')
    available_quantity = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Sales Rate')
    purchase_price_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1.30)
    history = HistoricalRecords()

    def __str__(self):
        return self.item_name + ' ' + '( ₹ ' + str(self.rate) + ' / ' + str(self.item_unit) + ' )'

    class Meta:
        verbose_name_plural = ' Items (Sales)'


class Tag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name
