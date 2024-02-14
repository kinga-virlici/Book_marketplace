from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from book_review.forms import BookReviewForm
from book_review.models.book_review import BookReview



class BookReviewView(View):
    model = BookReview
    template_name = 'book_review/book_review.html'

    def get(self, request):
        form = BookReviewForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BookReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')  # Replace with your success URL name
        return render(request, self.template_name, {'form': form})


class BookReviewList(ListView):
    model = BookReview
    template_name = 'book_review/book_review_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = context['object_list']
        return context
