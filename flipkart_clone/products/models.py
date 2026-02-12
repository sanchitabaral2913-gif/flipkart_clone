from django.db import models
from django.conf import settings
from accounts.models import User

# --------------------
# CATEGORY
# --------------------
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# --------------------
# PRODUCT
# --------------------
class Product(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()

    image_front = models.ImageField(upload_to='products/', blank=True, null=True)
    image_back = models.ImageField(upload_to='products/', blank=True, null=True)
    image_left = models.ImageField(upload_to='products/', blank=True, null=True)
    image_right = models.ImageField(upload_to='products/', blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # ⭐ Average rating (AUTO show)
    def average_rating(self):
        reviews = self.reviews.all()   # 🔥 STATUS FILTER HATA DIYA
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return 0

    def __str__(self):
        return self.name


# --------------------
# REVIEW
# --------------------
class Review(models.Model):

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    
    # ✅ Add status field
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # ✅ 1 user = 1 review

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
