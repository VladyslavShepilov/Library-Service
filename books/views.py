from rest_framework import viewsets

from books.serializers import BookSerializer, BookListSerializer

from books.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        return BookSerializer
