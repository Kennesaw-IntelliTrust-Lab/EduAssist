from django.urls import path
from django.urls import reverse
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('token/', views.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.login_view, name='login'),
    path('dashboard/<str:username>/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_view, name='upload'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
]
