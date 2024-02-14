from django.urls import path
from book_review.views import BookReviewView
from book_review.views import BookReviewList

# in acest fisier definim rutele specifice acestei functionalitati

app_name = 'book_review'

urlpatterns = [
    path('book_review/', BookReviewView.as_view(), name='book_review'),
    path('book_review_list', BookReviewList.as_view(), name='book_review_list')
]
