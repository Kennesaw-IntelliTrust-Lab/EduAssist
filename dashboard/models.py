from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import os

# Helper function to define upload paths
def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"

### 1. Assignments Model ###
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    due_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")

    def __str__(self):
        return self.title

### 2. Class Notes Model ###
class ClassNote(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="class_notes")

    def __str__(self):
        return self.title

### 3. Syllabus Model ###
class Syllabus(models.Model):
    course_name = models.CharField(max_length=255)
    file = models.FileField(upload_to="syllabus/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="syllabus")

    def __str__(self):
        return self.course_name

### 4. Chat Message Model ###
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"

### 5. Submission Model (For Student Assignment Submission) ###
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"