from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, Fine
from books.models import Book

import stripe


class CreatePaymentIntentView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        if book.inventory <= 0:
            return Response(
                {"error": "No books available!"}, status=status.HTTP_400_BAD_REQUEST
            )

        success_url = request.build_absolute_uri(reverse("payment_success"))
        cancel_url = request.build_absolute_uri(reverse("payment_cancel"))

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(book.daily_fee * 100),  # amount in cents
                currency="usd",
                description=f"Rental for {book.title} by {book.author}",
                metadata={
                    "book_id": book.id,
                    "title": book.title,
                    "author": book.author,
                },
            )
            Payment.objects.create(
                book=book, amount=book.daily_fee, stripe_session_id=payment_intent["id"]
            )
            return Response({"client_secret": payment_intent.client_secret})
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SuccessView(APIView):
    def get(self, request):
        session_id = request.GET.get("session_id")
        payment = get_object_or_404(Payment, stripe_session_id=session_id)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                payment.is_paid = True
                payment.save()
                return Response({"message": "Payment successful!"})
            else:
                return Response(
                    {"error": "Payment not completed!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CancelView(APIView):
    def get(self, request):
        return Response(
            {"message": "Payment canceled. You can try again within 24 hours."}
        )
