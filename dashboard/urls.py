from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Landing page
    path('', views.index, name='index'),  

    # User Registration and JWT Token Generation
    path('dashboard/register/', views.register_view, name='register'),
    path('token/', views.ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('dashboard/login/', views.login_view, name='login'),  # Login
    path('dashboard/logout/', views.logout_view, name='logout'),  # Logout

    # User-Specific Dashboard
    path('dashboard/<str:username>/', views.user_dashboard, name='user_dashboard'), 
    
    # Multiple couse
    path('api/add-course/', views.add_course, name='add_course'),
    path('api/delete-course/<int:course_id>/', views.delete_course, name='delete_course'), 

    # File Upload and Secure File Access
    path('file/<int:file_id>/', views.serve_file, name='serve_file'),

    # Delete file
    path('delete-file/<int:file_id>/', views.delete_file_view, name='delete_file'),

    # Chatbot API Endpoint
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/chat-history/', views.chat_history, name='chat_history'),

    # chat file uploads
    path('api/upload-chat-file/', views.upload_chat_file, name='upload_chat_file'),
    
    # generated files by chatbot
    path('api/generate-file/', views.generate_file, name='generate_file'),

]




