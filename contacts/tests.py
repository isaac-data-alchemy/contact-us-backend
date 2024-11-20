from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


# Create your tests here.
class ContactSubmissionModel(TestCase):
    def setUp(self):
        self.contact_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '+1234567890',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        self.contact = ContactSubmission.objects.create(**self.contact_data)

    def test_contact_submission_creation(self):
        self.assertTrue(isinstance(self.contact, ContactSubmission))
        self.assertEqual(self.contact.__str__(), f"{self.contact.name} - {self.contact.submitted_at.strftime('%Y-%m-%d %H:%M')}")

    def test_contact_submission_fields(self):
        for field, value in self.contact_data.items():
            self.assertEqual(getattr(self.contact, field), value)



