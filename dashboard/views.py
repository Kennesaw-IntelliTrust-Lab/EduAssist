from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    print("Rendering index page")
    return render(request, 'dashboard/index.html')


class UserRegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def login_view(request):
    print("Accessing login view")
    return render(request, 'dashboard/login.html')

def dashboard_view(request):
    print("Accessing dashboard view")
    if request.user.is_authenticated:
        return render(request, 'dashboard/dashboard.html')
    else:
        return render(request, 'dashboard/login.html', {'error': 'You must be logged in to view the dashboard'})

def upload_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/upload.html')
    else:
        return render(request, 'dashboard/login.html', {'error': 'You must be logged in to upload files'})

