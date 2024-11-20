from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from contacts.utils import send_contact_email
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class ContactFormView(APIView):
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

    def post(self, request):
        """
        Handles post requests for contact form submissions.
        """
        logger.info("Received contact form submission request")
        serializer = ContactSubmissionSerializer(data=request.data)

        if serializer.is_valid():
            logger.debug("Form data validated successfully")
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            subject = serializer.validated_data.get('subject', 'No subject')
            message = serializer.validated_data['message']

            try:
                # Save submission to the database
                submission = serializer.save()
                logger.info(f"Contact submission saved to database. ID: %d", submission.id)

                # Send email
                send_contact_email(name, email, phone_number, subject, message)
                logger.info(f"Contact email sent successfully for submission ID: %d", submission.id)

                return Response({'success': "Email sent successfully"}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Error processing contact submission: {str(e)}", exc_info=True)
                return Response({'Error': "Something went wrong. Please try again later."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning(F"Invalid form submission received: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

