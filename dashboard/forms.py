from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UploadedFile, Course

# ============================================================
# USER REGISTRATION FORM
class RegisterForm(UserCreationForm):
    """Custom user registration form."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# ============================================================
# FILE UPLOAD FORM
class FileUploadForm(forms.ModelForm):
    """Form to handle file uploads with categories."""
    class Meta:
        model = UploadedFile
        fields = ["file", "category"]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

# ADD COURSE FORM
class CourseForm(forms.ModelForm):
    """Form to handle course creation."""
    class Meta:
        model = Course
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter course name..."}),
        }
