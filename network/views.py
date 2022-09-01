from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json


from .models import User,NetworkPost,Profile


def index(request):
    return render(request, "network/index.html",{
        "posts":NetworkPost.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def post(request):
    if request.method=="POST":
        #retrieves content of new post.
        content=request.POST["content"]
        #retrieves user posted.
        user=request.user

        try:
            posted=NetworkPost.objects.create(user=user,content=content,).order_by('desc')
            posted.save()
            return HttpResponseRedirect(reverse("index"))
        except:
            HttpResponse("Error occured.")
       
@login_required
def profile(request,person):

    profile_person=User.objects.get(username=person)
    profile_posts=NetworkPost.objects.filter(user__username=person)
    
    active_followers=Profile.objects.filter(following=profile_person)

    if request.user in active_followers:
        current=False
    else:
        current=True
    

    if request.method=='POST':
        if request.POST.get("button")=="follow":
            add_follower=Profile.objects.get(user=profile_person)
            add_follower.following.add(request.user)
            current=False
                   
        elif request.POST.get("button")=="unfollow":
            remove_follower=Profile.objects.get(user=profile_person)
            remove_follower.following.remove(request.user)
            current=True

    
        
    if request.user==profile_person:
        return render(request,"network/profile.html",{
        "usern":profile_person,
        "posts":profile_posts,
        #refers to profiles being followed our user name
        "following":Profile.objects.filter(following=profile_person).count(),
        #refers to followers of username
        # "followers":Profile.objects.filter(user=profile_person).count()-1,
        "follow":False,
        "followed":current

    })

    else:
        return render(request,"network/profile.html",{
        "usern":profile_person,
        "posts":profile_posts,
        # "followers":(Profile.objects.filter(user=profile_person).count()-1),
        "following":Profile.objects.filter(following=profile_person).count(),
        "follow":True,
        "followed":current

    })
