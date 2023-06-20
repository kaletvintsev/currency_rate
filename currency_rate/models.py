from django.db import models


class Currency(models.Model):
    char_code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.char_code


class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    date = models.DateField()
    value = models.DecimalField(max_digits=14, decimal_places=4)

    class Meta:
        unique_together = ('currency', 'date')

    def __str__(self):
        return f"{self.currency.char_code} - {self.date}"