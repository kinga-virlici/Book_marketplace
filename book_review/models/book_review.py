from django.db import models


class BookReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    review_content = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)