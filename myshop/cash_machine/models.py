from django.db import models


class Item(models.Model):
    title = models.CharField(unique=True, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.title
