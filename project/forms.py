from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'status', 'created_by', 'assigned_to')

        widgets = {
            'created_by': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border',
                'disabled':'disabled',
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
        }

