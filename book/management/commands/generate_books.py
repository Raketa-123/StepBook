import os
import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from book.models import Book

fake = Faker()

class Command(BaseCommand):
    help = "Создает 30 тестовых книг с фейковыми данными, обложками и PDF-файлами"

    def handle(self, *args, **kwargs):
        # Очистка старых книг
        Book.objects.all().delete()

        for i in range(30):
            title = fake.sentence(nb_words=3)
            author = fake.name()
            description = fake.paragraph(nb_sentences=5)

            # Создание поддельной обложки
            cover_content = ContentFile(
                fake.image(size=(300, 400)),
                name=f"cover_{i+1}.jpg"
            )
            # Создание тестового PDF
            pdf_bytes = b"%PDF-1.4\n%Fake PDF for testing\n"
            pdf_file = ContentFile(pdf_bytes, name=f"book_{i+1}.pdf")

            Book.objects.create(
                title=title,
                author=author,
                description=description,
                cover=cover_content,
                file=pdf_file
            )

        self.stdout.write(self.style.SUCCESS("✅ 30 книг успешно созданы!"))
