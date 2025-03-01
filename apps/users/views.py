from django.shortcuts import render, redirect
from django.contrib.auth import login
from apps.users.forms import SignupForm

# Create your views here.
def index(request):
    return render(request, 'users/index.html')


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print("\n\nform:", form, "\n\n")
        print("\n\nform.is_valid():", form.is_valid(), "\n\n")
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)  # Automatically log in the user after signup
            return redirect("home")  # Redirect to home or dashboard
    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})