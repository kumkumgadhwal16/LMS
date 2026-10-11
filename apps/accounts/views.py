from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from apps.enrollments.models import Enrollment



User = get_user_model()

#register
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "STUDENT")

        if not username or not email or not password:
            messages.error(request, "All fields are required.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")

        elif role not in ["STUDENT", "INSTRUCTOR"]:
            messages.error(request, "Invalid role selected.")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
            )
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")

    return render(request, "accounts/register.html")

   

#user_login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")




login_required
@login_required
def dashboard(request):
    if request.user.role == "STUDENT":
        return render(request, "accounts/student_dashboard.html")

    elif request.user.role == "INSTRUCTOR":
        return render(request, "accounts/instructor_dashboard.html")

    elif request.user.role == "ADMIN":
        return render(request, "accounts/admin_dashboard.html")

    return render(request, "accounts/dashboard.html")
    return render(request, "accounts/dashboard.html")



#user_logout
def user_logout(request):
    logout(request)
    return redirect("login")