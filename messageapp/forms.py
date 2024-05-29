from django import forms

class UserForm(forms.Form):
    email = forms.EmailField(label="New Email")