from django.utils import timezone
from rest_framework import serializers

from referral_system.mixins import EmailVerificationMixin
from .models import ReferralCode
from django.contrib.auth.models import User


class ReferralCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for ReferralCode objects, allowing you to view referral codes.
    """

    class Meta:
        model = ReferralCode
        fields = ['code', 'expiration_date']
        read_only_fields = ['code', 'expiration_date']


class SignUpSerializer(serializers.ModelSerializer, EmailVerificationMixin):
    referral_code = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'referral_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new user. If a valid referral code is provided,
        associates the new user with this referral code.
        """
        referral_code_str = validated_data.pop('referral_code', None)
        user = User.objects.create_user(**validated_data)

        if referral_code_str:
            try:
                referral_code = ReferralCode.objects.get(code=referral_code_str, expiration_date__gte=timezone.now())
                referral_code.referrals.add(user)
                referral_code.save()
            except ReferralCode.DoesNotExist:
                raise serializers.ValidationError({"referral_code": "Invalid or expired referral code."})

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
