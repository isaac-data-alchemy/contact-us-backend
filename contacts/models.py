from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class ContactSubmissionManager(models.Manager):
    def get_by_natural_key(self,email):
        return self.get(email=email)

class ContactSubmission(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=200, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?(?:[0-9][ -]?){6,14}[0-9]$',
        message="Phone number must be entered with optional '+' and country code. Spaces and hyphens are allowed. Length should be between 7 and 15 digits."
    )
    phone_number = models.CharField(
        _("Phone number"),
        validators=[phone_regex],
        max_length=17,
        blank=False,
        null=False
    )
    message = models.TextField(_("Message"))
    submitted_at = models.DateTimeField(_("Submitted at"),auto_now_add=True)
    objects = ContactSubmissionManager()

    class Meta:
        verbose_name = _("Contact Submission")
        verbose_name_plural = _("Contact Submissions")
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['submitted_at']),
            models.Index(fields=['email']),
        ]
        # unique_together = (("email",),)
    def natural_key(self):
        return (self.email,)

    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
