from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from apps.users.forms import SignupForm, UserLoginForm

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
            return redirect("products:home")  # Redirect to home or dashboard
    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('products:home')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('users:login')
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})