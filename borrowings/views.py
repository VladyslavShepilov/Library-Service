from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.select_related("book")
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")
        queryset = self.queryset

        if self.serializer_class == BorrowingSerializer:
            queryset = queryset.select_related("user")

        if user_id:
            queryset = queryset.filter(user=user_id)

        if is_active:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(
                actual_return_date__isnull=is_active
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        elif self.action in ("retrieve", "return_book"):
            return BorrowingDetailSerializer

        return BorrowingSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Book already returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        book = borrowing.book
        book.return_book()

        serializer = BorrowingDetailSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)

