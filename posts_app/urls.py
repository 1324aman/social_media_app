from django.urls import path
from . import views


app_name = 'posts_app'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home' ),
	path('signup/', views.UserRegisterView.as_view(), name='signup' ),
    path('create_post/', views.CreatePostView.as_view(), name='create_post' ),
    path('edit_profile/', views.UpdateProfileView.as_view(), name='edit_profile'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile'),
    path('delete_post/<int:pk>', views.DeletePostView.as_view(), name='delete_post'),
    path('like/', views.like, name='like'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('detail_post/<int:id>', views.detail_post, name='detail_post'),
    path('edit_post/<int:pk>', views.UpdatePostView.as_view(), name='edit_post'),
    path('validate_username/', views.validate_username, name='validate_username'),
   




]
