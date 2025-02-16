from django import forms
from .models import Assignment, ClassNote, Syllabus

# Form for Assignments
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Form for Class Notes
class ClassNoteForm(forms.ModelForm):
    class Meta:
        model = ClassNote
        fields = ['title', 'description', 'file']

# Form for Syllabus
class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['course_name', 'file']
