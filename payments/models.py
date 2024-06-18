from django.db import models


class Payment(models.Model):
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.book.title} - {'Paid' if self.is_paid else 'Unpaid'}"


class Fine(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    days_overdue = models.PositiveIntegerField()
    fine_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=2.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_fine(self):
        return self.days_overdue * self.payment.book.daily_fee * self.fine_multiplier

    def __str__(self):
        return f"Fine for {self.payment.book.title} - {self.calculate_fine()}"
