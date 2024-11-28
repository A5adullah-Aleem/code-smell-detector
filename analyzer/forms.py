from django import forms

class CodeUploadForm(forms.Form):
    file = forms.FileField()
