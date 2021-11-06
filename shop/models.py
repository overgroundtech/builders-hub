from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    offer = models.BooleanField(default=False)
    discount = models.FloatField()
    in_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images", blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} {self.image.url}'


ORDER_STATUS = (
    ('pending', 'Pending'),
    ('transit', 'Transit'),
    ('delivered', 'Delivered')
)


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)
    payment = models.CharField(max_length=30)
    made_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=ORDER_STATUS[0][0])

    def __str__(self):
        return self.id

