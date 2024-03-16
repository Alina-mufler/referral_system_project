from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ReferralCode
from .serializers import ReferralCodeSerializer, SignUpSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ReferralCodeViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    Managing user referral codes.

    Supports creating a new referral code and deleting an existing one.
    It also provides an action to receive a referral code by email of the user.
    """
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCodeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overrides the create method to add additional validation:
        the user cannot create a new referral code if he already has an active one.
        """
        referral_code = ReferralCode.objects.filter(user=self.request.user).first()
        if referral_code and referral_code.expiration_date >= timezone.now():
            raise ValidationError({"error": "User already has an active referral code."})
        serializer.save(user=self.request.user)

    def get_object(self):
        """
        Current user's referral code object.

        Generates 404 if the object is not found.
        """
        return get_object_or_404(ReferralCode, user=self.request.user)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'email', openapi.IN_QUERY,
            description="Email of the user to receive the referral code for",
            type=openapi.TYPE_STRING
        )
    ])
    @action(detail=False, methods=['get'], url_path='get-by-email')
    def get_by_email(self, request):
        """
        Receive a referral code via user email.

        Returns an error if the user is not found or the referral code has expired.
        """

        email = request.query_params.get('email', None)
        if email is None:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        referral_code = ReferralCode.objects.filter(user=user).first()
        if referral_code is None or referral_code.expiration_date < timezone.now():
            return Response({"error": "Referral code has expired or does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(referral_code)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='referrals')
    def get_referrals(self, request, pk=None):
        """
        Returns a list of referrals for the referral code of the user with the given ID.
        """
        referral_code = get_object_or_404(ReferralCode, user__id=pk)
        referrals = referral_code.referrals.all()
        serializer = UserSerializer(referrals, many=True)
        return Response(serializer.data)


class SignUPViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for registering new users.

    Supports the creation (registration) of new users.
    If a referral code is provided, the new user will be associated with the referral.
    """
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
