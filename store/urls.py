from django.urls import path
from . import views
from .views import BlogView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, UserEditView
from django.urls import path, include
from django.shortcuts import redirect


# Redirect view to send users to the login page
def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path("", redirect_to_home),  # Root URL redirects to the login page
    path("home", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("tildelt_nummer/", views.tildelt_nummer, name="tildelt_nummer"),
    path("tjek_id/<str:pk>", views.tjek_id, name="tjek_id"),
    path("hangman/", views.hangman, name="hangman"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("stat_konkurrence/", views.stat_konkurrence, name="stat_konkurrence"),
    path("stat_konkurrence_admin/", views.stat_konkurrence_admin, name="stat_konkurrence_admin"),
    path("er_det_fredag/", views.er_det_fredag, name="er_det_fredag"),
    path("åamp/", views.åamp, name="åamp"),
    path("kreditmax/", views.kreditmax, name="kreditmax"),
    path("blog/", BlogView.as_view(), name="blog"),
    path("article/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("add_post/", AddPostView.as_view(), name="add_post"),
    path("article/edit/<int:pk>", UpdatePostView.as_view(), name="update_post"),
    path("article/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("edit_profile/", UserEditView.as_view(), name="edit_profile"),
    path('poke/', views.poke, name='poke'),
    path("dtfr/", views.dtfr, name="dtfr"),
    path("pause/", views.pause, name="pause"),








]
