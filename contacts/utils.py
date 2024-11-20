from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
import logging
import time
from functools import wraps
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

def mask_sensitive_data(data: str, visible_start: int=3, visible_end: int = 3) -> str:
    """Mask Sensitive log data leaving only a few characters visible."""
    if not data or len(data) <= visible_start + visible_end:
        return data
    return f"{data[:visible_start]}***{data[-visible_end:]}"


def timer_decorator(func: Callable) -> Callable:
    """Decorator to measure execution time of functions"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        logger.info(f"{func.__name__} took {execution_time:.3f} seconds to execute")

        return {
            'result': result,
            'execution_time': execution_time
        }
    return wrapper

@timer_decorator
def send_contact_email(name, email, phone_number, subject, message):
    """Sends an email with the contact form details."""
    try:
        logger.debug(f"Attempting to send contact email")
        email_start_time = time.perf_counter()
        send_mail(
            subject = f"Contact us Form Submission: {subject}",
            message=f"Message from {name} ({email}), {phone_number}:\n{message}",
            from_email=email,
            recipient_list=['contact_us@systemtech-ng.com'],
            fail_silently=False,
        )
        email_end_time = time.perf_counter()
        email_duration = email_end_time - email_start_time

        logger.debug(f"Email sent successfully in {email_duration:.3f} seconds")
    except Exception as e:
        logger.error(f"Failed to send contact email: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Message sending failed.Please try again later.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

