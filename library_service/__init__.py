from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

import stripe
from django.conf import settings

__all__ = ("celery_app",)

stripe.api_key = settings.PRIVATE_PAYMENT_KEY
