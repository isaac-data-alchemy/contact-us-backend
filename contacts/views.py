from django.db import IntegrityError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from smtplib import SMTPException
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from .utils import send_contact_email as send_email
from .utils import mask_sensitive_data as mask_email
import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ContactFormView(GenericAPIView):
    """API view for handling contact submission"""
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
    Handles POST requests for processing contact form submissions.

    This method validates the submitted form data, saves it to the database, and sends a confirmation
    email. It handles errors gracefully and provides appropriate responses based on the outcome.

    Args:
        request: The HTTP request object containing the submitted form data.

    Returns:
        Response: A DRF Response object with:
            - HTTP 200 OK status and success message if the submission is successful.
            - HTTP 400 Bad Request status with validation errors if the data is invalid.
            - HTTP 500 Internal Server Error status and error message if an exception occurs.

    Workflow:
        1. Logs the receipt of a contact form submission request.
        2. Validates the submitted data using the `ContactSubmissionSerializer`.
            - If valid:
                - Saves the submission to the database.
                - Sends a confirmation email using the extracted data.
            - If invalid:
                - Returns a 400 response with validation errors.
        3. Handles exceptions during data processing or email sending.
            - Logs the error and returns a 500 response with a generic error message.

    Raises:
        Exception: Logs and handles any exceptions that occur during the process.

    Logs:
        - Info: Logs key events such as receipt of a request, successful save, or email sent.
        - Debug: Logs detailed validation success.
        - Warning: Logs validation errors.
        - Error: Logs exceptions with traceback details.
    """
        # Log incoming requests 
        logger.info("Received contact form submission request")    
        serializer = ContactSubmissionSerializer(data=request.data)
        logger.debug(f"Form data validated")
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        phone_number = serializer.validated_data['phone_number']
        subject = serializer.validated_data.get('subject', 'No subject')
        message = serializer.validated_data['message']

        try:
            # mask incoming email data for logs
            masked_email = mask_email(email)
            submission = serializer.save()
            logger.info(
                f"Contact submission saved to database. ID: {submission.id} "
                f"Email: {masked_email}"
            )

            # Send email
            email_result = send_email(
                name=name,
                email=email,
                phone_number=phone_number,
                subject=subject,
                message=message
            )
            return Response({
                'success': "Email sent successfully",
            }, status=status.HTTP_200_OK)

        except IntegrityError as db_error:
            logger.error(
                f"Database error: {str(db_error)}, Email:{masked_email}", exc_info=False)
            return Response(
                    {'error': "Something went wrong . Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except SMTPException as email_error:
            logger.error(
                f"Email sending failed: {str(email_error)}, Email: {masked_email}",
                exc_info=False
            )
            return Response(
                {'error': "Email could not be sent. please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(
                f"Unexpected error: {str(e)}",
                exc_info=True # Use stack trace for internal debugging
            )
            return Response(
                {'error': "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        logger.warning(
            f"Invalid form submission received: {serializer.errors} "
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
