from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import uuid

from django.utils import timezone


def create_expiration_date():
    """Creates an expiration date for the referral code by adding 3 days to the current date."""
    return timezone.now() + timedelta(days=3)


class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=100,
                            default=uuid.uuid4,
                            unique=True,
                            verbose_name='Referral code')
    expiration_date = models.DateTimeField(
        'Referral code expiration date',
        default=create_expiration_date
    )
    referrals = models.ManyToManyField(
        User,
        related_name='referred_by',
        blank=True,
        verbose_name='Registered users',
    )

    def __str__(self):
        return f"{self.user}'s referral code"
