from django import forms

class urlform(forms.Form):
    url = forms.URLField(label='Youtube URL', max_length=100)