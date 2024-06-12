from django.db import models, transaction
from django.contrib.auth import get_user_model

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Borrowing: {self.book_id} by {self.user}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.book.rent_book()
            return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-borrow_date"]
