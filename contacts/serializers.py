from rest_framework import serializers
from .models import ContactSubmission
import logging
logger = logging.getLogger(__name__)

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone_number', 'subject', 'message']


    def validate(self, data):
        if not all([data.get('name'), data.get('email'), data.get('phone_number'), data.get('message')]):
            raise serializers.ValidationError("name, email, phone number, and message are required fields.")
            logger.warning("Validation error failed to complete required fields")
        existing = ContactSubmission.objects.filter(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number'],
            message=data['message']
        ).exists()
        if existing:
            logger.info("Flagged a submission for repetition")
            raise serializers.ValidationError("This submission already exists.")
        return data

