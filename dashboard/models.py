from django.db import models
from django.contrib.auth.models import User
from storages.backends.gcloud import GoogleCloudStorage

# CATEGORY CHOICES
CATEGORY_CHOICES = [
    ("assignments", "Assignments"),
    ("class_notes", "Class Notes"),
    ("syllabus", "Syllabus"),
    ("chatbot_files", "Chatbot Files"),
]


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name']  # Prevent duplicate course names per user
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"

# Create dedicated GCS storage instance with signing disabled
gcs_storage = GoogleCloudStorage(credentials=None, querystring_auth=False)

# Update the upload_to_gcs function
def upload_to_gcs(instance, filename):
    # Create path with user and course
    if instance.course:
        return f'{instance.user.username}/{instance.course.name}/{filename}'
    else:
        return f'{instance.user.username}/{filename}'  # Fallback for backward compatibility

# Update UploadedFile model
class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    file = models.FileField(upload_to=upload_to_gcs, storage=gcs_storage)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        course_name = self.course.name if self.course else "No Course"
        return f"{self.user.username} - {course_name} - {self.file.name}"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField(UploadedFile, blank=True, related_name='chat_messages')
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"