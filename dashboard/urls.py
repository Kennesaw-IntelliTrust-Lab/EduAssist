from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('token/', views.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
]
