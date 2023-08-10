from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListAPIView, UserCreateAPIView, UserRetrieveUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [

    path('', UserListAPIView.as_view(), name='user-list'),
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('user/<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
    path('user/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

]
