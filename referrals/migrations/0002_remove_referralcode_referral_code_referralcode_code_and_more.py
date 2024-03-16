# Generated by Django 4.2.11 on 2024-03-15 12:16

from django.conf import settings
from django.db import migrations, models
import referrals.models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("referrals", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="referralcode",
            name="referral_code",
        ),
        migrations.AddField(
            model_name="referralcode",
            name="code",
            field=models.CharField(
                default=uuid.uuid4,
                max_length=100,
                unique=True,
                verbose_name="Referral code",
            ),
        ),
        migrations.AddField(
            model_name="referralcode",
            name="referrals",
            field=models.ManyToManyField(
                blank=True,
                related_name="referred_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Registered users",
            ),
        ),
        migrations.AlterField(
            model_name="referralcode",
            name="expiration_date",
            field=models.DateTimeField(
                default=referrals.models.create_expiration_date,
                verbose_name="Referral code expiration date",
            ),
        ),
    ]
