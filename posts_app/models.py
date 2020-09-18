from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import User


User._meta.get_field('email')._unique = True


class Post(models.Model):
	text = models.CharField(max_length=500, blank=True,null=True)
	image = models.ImageField(upload_to='post_image', blank=False,null=False)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name='likes')

	class Meta:
		ordering = ['-created']

	def total_likes(self):
		return self.likes.count()

	def get_absolute_url(self):
		return reverse("posts_app:detail_post", args=[self.id])

	def comments_count(self):
		comments = Comment.objects.filter(post=self).count()
		return comments



class Profile(models.Model):
	owner = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='profile_image')
	status = models.CharField(max_length=200,blank=True,null=True, default='this is you status')
	following = models.ManyToManyField(User, related_name='following')

	def total_followers(self):
		return self.following.count()


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	content = models.CharField(max_length=400,blank=False,null=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')

	class Meta:
		ordering = ['-timestamp']


