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
    #path('dashboard/', views.dashboard, name='dashboard'),  
    # path('upload/', views.upload_view, name='upload'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/assignment/', views.upload_assignment, name='upload_assignment'),
    path('upload/note/', views.upload_class_note, name='upload_class_note'),
    path('upload/syllabus/', views.upload_syllabus, name='upload_syllabus'),
    path('assignments/', views.view_assignments, name='view_assignments'),
    path('notes/', views.view_notes, name='view_notes'),
    path('syllabus/', views.view_syllabus, name='view_syllabus'),
]
