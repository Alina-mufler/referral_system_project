from djoser.serializers import UserCreateSerializer
from referral_system.mixins import EmailVerificationMixin
from rest_framework import serializers


class CustomUserCreateSerializer(EmailVerificationMixin, UserCreateSerializer):
    email = serializers.EmailField(required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('email',)
