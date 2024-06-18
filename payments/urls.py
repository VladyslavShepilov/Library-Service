from django.urls import path
from payments.views import CreatePaymentIntentView, SuccessView, CancelView

urlpatterns = [
    path(
        "create-payment-intent/<int:book_id>/",
        CreatePaymentIntentView.as_view(),
        name="create_payment_intent",
    ),
    path("success/", SuccessView.as_view(), name="payment_success"),
    path("cancel/", CancelView.as_view(), name="payment_cancel"),
]
