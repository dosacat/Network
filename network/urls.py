
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #to create a new post:
    path("post",views.post, name="post"),
    #to view a specific profiel:
    path("<str:person>",views.profile, name="all"),

    # #API routes:
    # path("posts/<int:post_id>",views.posted,name="posted")


]
