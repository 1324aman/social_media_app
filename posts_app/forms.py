from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from .models import Post, Profile, Comment
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'validate','placeholder': 'email or username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))


class SignupForm(UserCreationForm):
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))
	password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder':'password'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder':'email'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'first_name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'last_name'}))

	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-6'
	helper.field_class = 'col-lg-6'
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
		help_texts = {

            'username': None,
        }


class PostCreateForm(forms.ModelForm):
	text = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'message'}))
	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-2'
	helper.field_class = 'col-lg-8'
	
	class Meta:
		model = Post
		fields = ['text', 'image']


class UpdateProfileForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-2'
	helper.field_class = 'col-lg-8'
	
	class Meta:
		model = Profile
		fields = [ 'image', 'status']


class UpdateUserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
	content = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'comment here'}))
	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-2'
	helper.field_class = 'col-lg-8'
	
	class Meta:
		model = Comment
		fields = ['content']