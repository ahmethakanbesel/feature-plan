import time

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from hashid_field import HashidAutoField


# Create your models here.


class Category(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    slug = models.SlugField(default='', null=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def clean(self):
        self.name = self.name.strip()


class Product(models.Model):
    id = HashidAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(default='', null=True, unique=True, editable=False)
    logo = models.ImageField(null=True, blank=True,
                             default='/placeholder.png')
    websiteUrl = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    allowNewRequest = models.BooleanField(default=True)
    allowAnonymousVote = models.BooleanField(default=True)
    featureOrder = models.IntegerField(default=0, null=False)
    primaryColor = models.CharField(max_length=16, null=True, blank=True)
    secondaryColor = models.CharField(max_length=16, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField(default=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        #self.hash = Product.objects.latest('id') + 1 * 12345 + self.owner.id * 88 + 2021
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()

    def __str__(self):
        return self.name


class FeatureType(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(max_length=512, null=True, blank=True)
    color = models.CharField(max_length=16, null=False, blank=False)


class FeatureStatus(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(max_length=512, null=True, blank=True)
    color = models.CharField(max_length=16, null=False, blank=False)


class Feature(models.Model):
    id = HashidAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(default='', null=True, unique=True, editable=False)
    description = models.TextField(max_length=512, null=True, blank=True)
    type = models.ForeignKey(FeatureType, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(FeatureStatus, on_delete=models.SET_NULL, null=True, blank=True)
    votes = models.IntegerField(default=0)
    public = models.BooleanField(default=True)
    createdBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Comment(models.Model):
    id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=False)
    content = models.TextField(default='')
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())


class Vote(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=False)
    ip = models.GenericIPAddressField(null=True, blank=True, db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, getattr(self, field.name).strip())


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
