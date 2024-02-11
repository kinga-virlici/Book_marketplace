from django import forms
from book_review.models.book_review import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['reviewer_name', 'book_title', 'image', 'review_content']