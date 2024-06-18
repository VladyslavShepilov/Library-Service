from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from borrowings.models import Borrowing
from notifications.telegram import send_telegram_message
import logging

logger = logging.getLogger(__name__)


@shared_task
def check_overdue_borrowings_and_notify():
    try:
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        overdue_borrowings = Borrowing.objects.select_related("user").filter(
            expected_return_date__lte=tomorrow,
            actual_return_date__isnull=True
        )

        overdue_borrowings_count = overdue_borrowings.count()
        logger.info(f"Found {overdue_borrowings_count} overdue borrowings.")

        if overdue_borrowings.exists():
            for borrowing in overdue_borrowings:
                message = f"Borrowing #{borrowing.id} is overdue. Please return the book {borrowing.book.title}."
                send_telegram_message(message)
                logger.info(f"Sent notification for borrowing #{borrowing.id}.")
            return f"Sent notifications for {overdue_borrowings_count} overdue borrowings."
        else:
            return "No borrowings overdue today."
    except Exception as e:
        logger.error(f"Error in check_overdue_borrowings_and_notify task: {str(e)}")
        return f"Error in check_overdue_borrowings_and_notify task: {str(e)}"
