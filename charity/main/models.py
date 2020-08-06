from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)


TYPES = (
    ("fundacja", "fundacja"),
    ("organizacja pozarządowa", "organizacja pozarządowa"),
    ("zbiórka lokalna", "zbiórka lokalna")
)


class Institution(models.Model):
    name = models.CharField(max_length=90)
    description = models.CharField(max_length=255)
    type = models.CharField(choices=TYPES, default="fundacja", max_length=64)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=255, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="user", default=None, null=True)
