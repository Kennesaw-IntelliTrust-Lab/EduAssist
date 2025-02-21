from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    print("Rendering index page")
    return render(request, 'dashboard/index.html')


#View


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Render the registration form
        return render(request, 'dashboard/register.html')

    def post(self, request):
        # Process registration form data
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            # Redirect to login page after successful registration
            return redirect('/dashboard/login/')
        # Return errors if registration fails
        return render(request, 'dashboard/register.html', {'errors': serializer.errors})


#View


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



#View

'''
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate token and store it in a cookie
            refresh = RefreshToken.for_user(user)
            response = redirect('/dashboard/dashboard/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            return response
        else:
            # Invalid credentials, reload login page with error
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})
    return render(request, 'dashboard/login.html')
'''

def login_view(request):
    if request.method == 'POST':
        # Retrieve credentials from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Log in the user
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Redirect to the user's specific dashboard
            response = redirect(reverse('user_dashboard', kwargs={'username': user.username}))

            # Set JWT tokens as HTTP-only cookies
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)  # Optional refresh token

            return response
        else:
            # Invalid credentials, reload login page with error
            return render(request, 'dashboard/login.html', {'error': 'Invalid username or password'})

    # Render login page for GET requests
    return render(request, 'dashboard/login.html')

#View


def dashboard_view(request):
    try:
        auth = JWTAuthentication()
        auth.authenticate(request)
        return render(request, 'dashboard/dashboard.html')
    except AuthenticationFailed:
        return redirect('/dashboard/login/')


@login_required
def user_dashboard(request, username):
    # Ensure the logged-in user is accessing their own dashboard
    if request.user.username != username:
        return redirect('login')  # Redirect to login if unauthorized access is attempted

    # Example: Fetch user-specific data (customize as needed)
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        # Add more user-related data here if needed
    }

    return render(request, 'dashboard/dashboard.html', {'user_data': user_data})

#View

def upload_view(request):
    try:
        auth = JWTAuthentication()
        auth.authenticate(request)
        return render(request, 'dashboard/upload.html')
    except AuthenticationFailed:
        return redirect('/dashboard/login/')


#View


def logout_view(request):
    # Clear the JWT token by deleting the cookie
    response = redirect('/dashboard/login/')  # Redirect to the login page
    response.delete_cookie('access_token')    # Remove the JWT token from the cookies
    messages.success(request, 'You have been logged out successfully.')
    return response