from django import forms
from .models import Task

class Taskform(forms.ModelForm):
    class Meta:
        model = Task
        fields=["title","description","important"]
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control","placeholder":"Escriba el titulo"}),
            "description": forms.Textarea(attrs={"class":"form-control","placeholder":"Escriba la descripcion"}),
            "important": forms.CheckboxInput(attrs={"class":"form-check-input text-center"}),
        }