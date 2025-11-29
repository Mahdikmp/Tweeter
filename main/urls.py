from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', views.home, name='home'),
    path('profiles_list', views.profiles_list, name='profiles_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register, name='register'),
    path('edit_profile/', views.editProfile, name='edit_profile'),
    path('password_change/', views.passwordChange, name='password_change'),
    path('profile_image/', views.profileImageUpdate, name='profile_image'),
    path('tweet/<int:tweet_id>/like/', views.like, name='tweetLike'),
    path('tweet/<int:pk>/', views.tweetShow, name='tweet'),
    path('tweet/<int:pk>/delete/', views.tweetDelete, name='tweet_delete'),
    path('tweet/<int:pk>/edit/', views.tweetEdit, name='tweet_edit'),
    path('follow/<int:user_id>/', views.follow, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unFollow, name='unfollow_user'),
    path('profile/<int:pk>/followers/', views.userFollowers, name='user_followers'),
    path('profile/<int:pk>/followeings/', views.userFollowings, name='user_followings'),
    path('user_search/', views.userSearch, name='user_search'),

    # ------------------ Password Reset Urls ---------------------

path('reset-password/', PasswordResetView.as_view(
        template_name='passReset/pass_reset.html'
    ), name='reset_password'),

    path('reset-password/done/', PasswordResetDoneView.as_view(
        template_name='passReset/pass_reset_sent.html'
    ), name='password_reset_done'),

    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='passReset/pass_reset_form.html'
    ), name='password_reset_confirm'),

    path('reset-password/complete/', PasswordResetCompleteView.as_view(
        template_name='passReset/pass_reset_done.html'
    ), name='password_reset_complete'),
]