from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError
from django.contrib.auth import get_user_model

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def is_active(self):
        return self.actual_return_date is None

    def __str__(self):
        return f"{self.book.title} by {self.user.email}"

    def clean(self):
        if (
            self.actual_return_date is not None
            and self.expected_return_date <= self.borrow_date
        ):
            raise ValidationError("Expected return date must be after borrow date.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.clean()
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["-borrow_date"]
