import stripe
from django.db import models

from payments.models import Fine, Payment


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def rent_book(self, error):
        if self.inventory >= 1:
            self.inventory -= 1
            self.save()
        else:
            raise error("No books available!")

    def return_book(self):
        self.inventory += 1
        self.save()

    # Sync with remote stripe service
    def sync_with_stripe(self):
        if not self.stripe_product_id:
            product = stripe.Product.create(
                name=self.title,
                description=f"{self.title} by {self.author}, {self.get_cover_display()}",
                metadata={"author": self.author, "cover": self.cover},
            )
            self.stripe_product_id = product.id

        if not self.stripe_price_id:
            price = stripe.Price.create(
                unit_amount=int(self.daily_fee * 100),  # amount in cents
                currency="usd",
                product=self.stripe_product_id,
            )
            self.stripe_price_id = price.id

        self.save()

    def check_fine(self, actual_return_date, expected_return_date):
        if actual_return_date > expected_return_date:
            days_overdue = (actual_return_date - expected_return_date).days
            fine_amount = (
                days_overdue * self.daily_fee * 2
            )  # Assuming FINE_MULTIPLIER is 2
            Payment = apps.get_model("payments", "Payment")
            Fine = apps.get_model("payments", "Fine")
            payment = Payment.objects.create(book=self, amount=fine_amount)
            Fine.objects.create(
                payment=payment, days_overdue=days_overdue, fine_multiplier=2
            )
            return payment
        return None

    class Meta:
        unique_together = ("title", "author")
        ordering = ["-daily_fee"]
