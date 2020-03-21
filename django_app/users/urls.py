from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserAPIView.as_view()),
    path('', views.UserRetrieveUpdateAPIView.as_view()),
    path('all/', views.GetAllUsersAPIView.as_view()),
    path('refresh_token/', views.RefreshToken.as_view()),
]
