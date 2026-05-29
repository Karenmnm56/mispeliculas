from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Movie, Category


# =========================
# 🧾 REGISTER FORM
# =========================
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_seller', 'password1', 'password2')


# =========================
# 🎬 MOVIE FORM
# =========================
class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = [
            'title',
            'description',
            'price',
            'stock',
            'image',
            'categories'
        ]

        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }