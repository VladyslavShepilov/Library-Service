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

    @staticmethod
    def validate_creation_time(borrow_date, expected_return_date, actual_return_date, error):
        if expected_return_date < borrow_date:
            raise error("Return date can't be less than borrow date!")
        if actual_return_date and actual_return_date < borrow_date:
            raise error("Actual return date can't be less than borrow date!")

    def clean(self):
        self.validate_creation_time(
            self.borrow_date,
            self.expected_return_date,
            self.actual_return_date,
            IntegrityError
        )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.clean()
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["-borrow_date"]
