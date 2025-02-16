from django.contrib import admin
from .models import Assignment, ClassNote, Syllabus, ChatMessage, Submission
# Register your models here.


admin.site.register(Assignment)
admin.site.register(ClassNote)
admin.site.register(Syllabus)
admin.site.register(ChatMessage)
admin.site.register(Submission)
