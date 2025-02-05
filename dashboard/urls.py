from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('token/', views.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_view, name='upload'),
]
