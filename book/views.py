from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from book.models import Book
from book.serializers import BookSerializer

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View
from book.forms import BookForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

def home_page(request):
    books_list = Book.objects.all().order_by('-id')
    paginator = Paginator(books_list, 9)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'home.html', {'books': books})

class SearchPage(View):
    template_name = 'search.html'

    def get(self, request):
        query = request.GET.get('q', '')
        books = Book.objects.all()

        if query:
            books = books.filter(title__icontains=query)

        paginator = Paginator(books, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'books': page_obj,
            'query': query,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user

        context['purchased'] = user.is_authenticated and (book in user.purchased_books.all() or book.owner == user)

        return context



@login_required
def buy_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    if book.owner == user:
        messages.warning(request, "Нельзя купить свою собственную книгу.")
        return redirect('book_detail', pk=book.id)

    if book not in user.purchased_books.all():
        user.purchased_books.add(book)
        messages.success(request, "Книга успешно куплена!")

    return redirect('book_detail', pk=book.id)


class AddBookView(View):
    template_name = 'add_book.html'

    def get(self, request):
        form = BookForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('home_page')
        return render(request, self.template_name, {'form': form})


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.owner != request.user:
        return HttpResponseForbidden("Вы не можете удалить чужую книгу.")

    if request.method == "POST":
        book.delete()
        messages.success(request, "Книга успешно удалена.")
        return redirect('home_page')

    return render(request, 'delete_book.html', {'book': book})
