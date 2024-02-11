from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from book_review.forms import BookReviewForm
from book_review.models.book_review import BookReview


class BookReviewView(ListView):
    model = BookReview
    template_name = 'book_review/book_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_review'] = context['object_list']
        return context


def book_review(request):
    if request.method == "GET":
        form = BookReviewForm
        context = {
            "form": form
        }
        return render(request, 'templates/book_review.html', context=context)
    elif request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BookReviewForm()
    return render(request, 'book_review.html', {'form': form})
