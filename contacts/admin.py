from django.contrib import admin
from .models import ContactSubmission
from rest_framework.response import Response


# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'submitted_at')
    list_filter = ('email', 'submitted_at')
    search_fields = ('email',)
admin.site.register(ContactSubmission, ContactAdmin)