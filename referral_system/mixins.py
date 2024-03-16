from rest_framework import serializers
from django.contrib.auth import get_user_model
import requests

from referral_system import settings

User = get_user_model()


def verify_email_with_hunter(email):
    """Checking email using Hunter.io."""
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data']['result'] == 'deliverable'
    return False


class EmailVerificationMixin:
    """Mixin to add email verification to serializers."""

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")

        if not verify_email_with_hunter(value):
            raise serializers.ValidationError("This email is not deliverable according to Hunter.io.")
        return value
