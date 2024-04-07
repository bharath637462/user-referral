from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import User
from .serializers import UserSerializer, ReferralSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegistrationAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response("User registered successfully", UserSerializer)},
    )
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user_id': serializer.data['id'],
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("User details", UserSerializer)},
        security=[{"BearerAuth": []}],
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ReferralsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("List of referrals", ReferralSerializer)},

    )
    def get(self, request):
        # Get current user
        current_user = request.user

        # Get referrals of the current user
        referrals = User.objects.filter(referral_code=current_user.id)

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(referrals, request)

        # Serialize the data
        serializer = ReferralSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
