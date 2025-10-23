from django.views.generic import DetailView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from pdf2image import convert_from_path
import os
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    published_date = models.DateField(default=timezone.now)
    file = models.FileField(upload_to='books/', blank=True, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=False)
    cover = models.ImageField(upload_to='covers/', blank=True, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_books', null = True)


@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user

        context['purchased'] = book in user.purchased_books.all()

        pdf_preview_path = None
        if book.file and book.file.name.endswith('.pdf'):
            pdf_path = book.file.path
            preview_filename = f"preview_{book.id}.jpg"
            preview_path = os.path.join(settings.MEDIA_ROOT, "previews", preview_filename)
            preview_url = f"{settings.MEDIA_URL}previews/{preview_filename}"

            os.makedirs(os.path.dirname(preview_path), exist_ok=True)

            if not os.path.exists(preview_path):
                try:
                    images = convert_from_path(pdf_path, first_page=1, last_page=1)
                    images[0].save(preview_path, "JPEG")
                except Exception as e:
                    print("Ошибка при создании превью PDF:", e)

            pdf_preview_path = preview_url

        context["pdf_preview"] = pdf_preview_path
        return context

@login_required
def buy_book(request, pk):
    book = Book.objects.get(pk=pk)
    user = request.user

    if book not in user.purchased_books.all():
        user.purchased_books.add(book)

    return redirect('book_detail', pk=book.id)
