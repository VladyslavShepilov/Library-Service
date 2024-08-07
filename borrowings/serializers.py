from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import ValidationError
from datetime import datetime

from borrowings.models import Borrowing
from books.serializers import (
    BookListSerializer,
    BookSerializer
)
from notifications.telegram import send_telegram_message


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date",
            "expected_return_date", "actual_return_date",
            "book", "user"
        )

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        attrs["borrow_date"] = datetime.now().date()
        Borrowing.validate_creation_time(
            attrs["borrow_date"], attrs["expected_return_date"], attrs["actual_return_date"],
            ValidationError
        )
        return data

    def create(self, validated_data):
        try:
            with transaction.atomic():
                book = validated_data.pop("book")
                book.rent_book(ValidationError)

                borrowing = Borrowing.objects.create(book=book, **validated_data)

                message = (
                    f"Book {borrowing}. Expected return date {validated_data['expected_return_date']}."
                )
                send_telegram_message(message)

                return borrowing
        except ValidationError as e:
            raise serializers.ValidationError(str(e))


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookListSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date",
            "actual_return_date", "book",
            "is_active", "user",
        )


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date",
            "actual_return_date", "book",
            "is_active", "user",
        )
