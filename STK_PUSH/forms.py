from django import forms
from .models import Meetings, SignUp, RegisterChama, Article

class Meet(forms.Form):
    venue = forms.CharField(max_length=60)
    date = forms.DateField()
    time = forms.TimeField()

    def __init__(self, *args, **kwargs):
        super(Meet, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    name_of_chama = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-group'

class RegisterChamaForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    name_of_chama = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=50)
    email = forms.EmailField()
    id_number = forms.IntegerField()
    county = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegisterChamaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-group'

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200)
    headline = forms.CharField(max_length=300)
    link = forms.URLField(max_length=500)
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'