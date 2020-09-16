from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from .models import Post, Profile, Comment

class SignupForm(UserCreationForm):
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-6'
	helper.field_class = 'col-lg-6'
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
		labels = {'email':'Email'}
		help_texts = {

            'username': None,
        }

class PostCreateForm(forms.ModelForm):
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
	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-2'
	helper.field_class = 'col-lg-8'
	
	class Meta:
		model = Comment
		fields = ['content']