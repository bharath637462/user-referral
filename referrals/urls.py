from django.urls import path

from core.utills import get_api_url
from .views import (
    UserRegistrationAPIView,
    UserDetailsAPIView,
    ReferralsAPIView
    )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path(get_api_url(app_name='user-registration'), UserRegistrationAPIView.as_view(), name='user-registration'),
    path(get_api_url(app_name='user-detail'), UserDetailsAPIView.as_view(), name='user-details'),
    path(get_api_url(app_name='user-referrals-list'), ReferralsAPIView.as_view(), name='referrals-list'),

]
