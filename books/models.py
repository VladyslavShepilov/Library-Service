from django.db import models


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

    class Meta:
        unique_together = ("title", "author")
        ordering = ["-daily_fee"]
