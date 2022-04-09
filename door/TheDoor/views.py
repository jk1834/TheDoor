from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm
from .models import Profile, UserPost
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, "base.html")


# Handles the lsit of posts from other users, and saves posts made by users to their profiles
def dashboard(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("The Door:dashboard")

    # Sorts the posts by when they were posted
    followed_posts = UserPost.objects.filter(
        user__profile__in=request.user.profile.friends.all()
    ).order_by("-created_at")

    return render(
        request, "TheDoor/dashboard.html", {"form": form, "posts": followed_posts}
    )


# Simply creates the list of profiles and redirects the user to the profile list page
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "TheDoor/profile_list.html", {"profiles": profiles})


# Goes to specific user profile instead of viewing all of them once clicked on
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)

    # Makes sure the suer exists
    if not hasattr(request.user, "profile"):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    # Handles the friending and unfriending of users
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")

        if action == "follow":
            current_user_profile.friends.add(profile)
        elif action == "unfollow":
            current_user_profile.friends.remove(profile)

        current_user_profile.save()
    return render(request, "TheDoor/profile.html", {"profile": profile})


def signout(request):

    # Simply logs out
    logout(request)
    messages.success(request, "Logged out successfully.")
    return render(request, "base.html")


# Checks for special characters in passwords
def is_special_character(password):
    special_char = "!@#$%^&*-_./"
    if any(password in special_char for password in special_char):
        return True
    return False


# Handles all signup functionality
def signup(request):

    if request.method == "POST":
        # Records all information needed for checks and user creation
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = None
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        # Checks if username has already been taken
        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken.")
            return render(request, "TheDoor/signup.html")

        # VALIDATION GOES HERE
        # Makes sure that all characters in username are only alphanumeric
        if not username.isalnum():
            messages.error(
                request, "Make sure your username only contains numbers and letters."
            )
            return render(request, "TheDoor/signup.html")

        # Makes sure the password falls under specified character conditions
        if (not is_special_character(pass1)) or len(pass1) <= 8:
            messages.error(
                request,
                'Your password must include at least one of the following: "! @ # $ % ^ & * - _ . /" You must also include at least 8 characters.',
            )
            return render(request, "TheDoor/signup.html")

        # Makes sure the user's name only has alphabetical letters
        if (not firstname.isalpha()) or (not lastname.isalpha()):
            messages.error(
                request, "Your first and last name must only include the letters a-z."
            )
            return render(request, "TheDoor/signup.html")

        # Makes a new user and assigns basic properties, then saves that information to the Django database
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        Profile(myuser).save()
        myuser.save()

        # Outputs success message and redirects user to the sign in page
        messages.success(request, "Your account has been successfully created!")

        return render(request, "TheDoor/signin.html")
    return render(request, "TheDoor/signup.html")


# Handles login functionality
def signin(request):

    if request.method == "POST":

        # Retrieves information from database
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        # Checks if the information entered is in the database
        user = authenticate(username=username, password=pass1)

        # If the user exists, log them in and show them to the main page
        if user is not None:
            login(request, user)
            return render(request, "TheDoor/dashboard.html")

        # Else, return them to the home page with an error
        else:
            messages.error(request, "Incorrect Username or Password")
            return render(request, "TheDoor/signin.html")

    return render(request, "TheDoor/signin.html")
