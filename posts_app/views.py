from posts_app.forms import CustomAuthForm
from django.template.loader import render_to_string
from django.shortcuts import (
	render, HttpResponseRedirect,redirect,
	reverse, get_object_or_404
)
from .forms import (
 SignupForm, PostCreateForm, UpdateProfileForm,
  UpdateUserForm, CommentForm
 )
from django.contrib.auth.forms import(
	AuthenticationForm
	)
from django.contrib.auth import(
	authenticate, login,
	logout
	)
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView
from .models import Post, Profile, Comment
import datetime
from django.views.generic.edit import DeleteView 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator


class HomeView(LoginRequiredMixin, ListView):
	login_url = 'login'
	model = Post
	template_name = 'posts_app/home.html'
	paginate_by = 5

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['following_profile_list'] = Profile.objects.filter(following__in=[self.request.user.id])
		return context


class DeletePostView(LoginRequiredMixin, DeleteView):
	login_url = 'login'
	model = Post
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.owner == self.request.user:
			self.object.delete()
			data = {
			'deleted':'yes'
			}
			return JsonResponse(data)


class ProfileDetailView(LoginRequiredMixin, DetailView):
	login_url = 'login'
	model = Profile
	template_name = 'posts_app/profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.get(id=self.object.owner.id)
		context['post_list'] = Post.objects.filter(owner=self.object.owner)
		return context

	
class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	login_url = 'login'
	model = Post
	form_class = PostCreateForm
	template_name = 'posts_app/edit_post.html'

	def get_success_url(self):
		return reverse("posts_app:detail_post", args=[self.object.id])

	def test_func(self):
		obj = self.get_object()
		return obj.owner == self.request.user


class FollowView(View):

	def get(self, request):
		profile = get_object_or_404(Profile, id=request.GET.get('profile_id'))
		following = False

		if profile.following.filter(id=request.user.id).exists():
			profile.following.remove(request.user)
			following = False
		else:
			profile.following.add(request.user)
			following = True

		data = {
		'following':following
		}
		return JsonResponse(data)


def like(request):
	post= get_object_or_404(Post, id= request.GET.get('post_id'))
	
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked=False
	else:
		post.likes.add(request.user)
		is_liked=True
	data = {
		'is_liked': is_liked,
		'total_likes': post.total_likes()
	}
	return JsonResponse(data)



class UserRegisterView(CreateView):
	model = User
	form_class = SignupForm
	template_name = 'posts_app/signup.html'
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		user = form.save(commit=False)
		user.save()
		Profile.objects.create(owner=user)
		return redirect('login')


def user_login(request):
	if request.method == 'POST':
		form = CustomAuthForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request,'logged in successfully')
				next_url = request.GET.get("next")
				if next_url:
					return HttpResponseRedirect(next_url)
				return redirect('posts_app:home')
	else:
		form = CustomAuthForm()
	return render(request, 'posts_app/login.html', {'form':form})


class CreatePostView(LoginRequiredMixin, CreateView):
	login_url = 'login'
	model = Post
	form_class = PostCreateForm
	template_name = 'posts_app/create_post.html'

	def form_valid(self, form):
		post = form.save(commit=False)
		post.owner = self.request.user
		post.save()
		return redirect('posts_app:home')


class UpdateProfileView(LoginRequiredMixin, View):
	login_url = 'login'
	template_name = 'posts_app/edit_profile.html'
	form_class1 = UpdateUserForm
	form_class2 = UpdateProfileForm

	def get(self, request):
		user_form = self.form_class1(instance=request.user)
		profile_form = self.form_class2(instance=request.user.profile)
		context = {
		'user_form': user_form,
		'profile_form': profile_form
		}
		return render(request, self.template_name, context)

	def post(self, request):
		user_form = self.form_class1(request.POST, instance=request.user)
		profile_form = self.form_class2(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect('posts_app:profile', request.user.profile.id)		


@login_required(login_url='login')
def detail_post(request, id):
	post = get_object_or_404(Post , id=id)
	if request.method=='POST':
		form=CommentForm(request.POST or None)

		if form.is_valid():
			comment_id = request.POST.get('comment-id')
			comment_obj =None
			if comment_id:
				comment_obj = Comment.objects.get(id=comment_id)
			content=request.POST.get('content')
			comment=Comment.objects.create(post=post, owner=request.user, content=content, reply=comment_obj)
			comment.save()
	comments= Comment.objects.filter(post=post, reply=None).order_by('-id')
	context={
	'form': CommentForm(),
	'post': post,
	'comments': comments,
	 }

	if request.is_ajax():
		html=render_to_string('posts_app/comment.html', context, request=request)
		return JsonResponse({'form': html })

	return render(request, 'posts_app/detail_post.html', context)


def validate_username(request):
	username = request.GET.get('username')
	data={
	'username_exists':User.objects.filter(username=request.GET.get('username')).exists()
	}
	return JsonResponse(data)

	
def user_logout(request):
	logout(request)
	return redirect('login')