from rest_framework import viewsets
from book.models import Book
from book.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

def home_page(request):
    books = Book.objects.all()
    return render(request, 'home.html', {"books": books})

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user
        context['purchased'] = user.is_authenticated and book in user.purchased_books.all()
        return context

@login_required
def buy_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    if book not in user.purchased_books.all():
        user.purchased_books.add(book)

    return redirect('book_detail', pk=book.id)
