from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from borrowings.models import Borrowing
from books.models import Book


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date",
            "actual_return_date", "book",
            "user"
        )

    def create(self, validated_data):
        with transaction.atomic():
            book_id = validated_data.get("book")
            book = get_object_or_404(Book, book_id)

            book.rent_book(ValidationError)
            borrowing = Borrowing.objects.create(**validated_data)

            return borrowing
