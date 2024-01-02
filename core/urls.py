from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name='index'),
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name='signin'),
    path("logout/", views.logout, name='logout'),
    path("setting/", views.setting, name='setting'),

    path("upload", views.upload, name='upload'),

    path("like-post", views.like_post, name='like-post'),

    path("userProfile/<str:pk>", views.userProfile, name='userProfile'),

    path("follow", views.follow, name='follow'),

    path("search", views.search, name='search'),
    path("password_reset/", auth_views.PasswordResetView.as_view() , name='password_reset'),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view() , name='password_reset_done'),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view() , name='password_reset_complete'),

    
]
 