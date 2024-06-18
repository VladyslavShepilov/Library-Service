from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user"), include("users.urls", namespace="users"),
    path("api/books/", include("books.urls", namespace="books")),
    path(
        "api/borrowings/",
        include("borrowings.urls", namespace="borrowings"),
    ),
    path("payments/", include("payments.urls")),
]
