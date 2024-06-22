# No seu arquivo forms.py
from django import forms
from .models import ToDoList, ToDoItem

class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title']  
