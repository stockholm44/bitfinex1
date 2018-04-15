from django.db import models
from django.utils import timezone
# from .FinexAPI import bid

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Price_Coin(models.Model):
    name = models.CharField(max_length=5)
    price_usd = models.CharField(max_length=10)
    price_krw = models.CharField(max_length=10)
    exchange_rate = models.CharField(max_length=10)
    gimp = models.CharField(max_length=10)
    volume = models.CharField(max_length=10)
    website = models.URLField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['volume']
