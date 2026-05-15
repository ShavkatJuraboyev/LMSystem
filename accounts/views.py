from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

 
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            "Login yoki parol noto‘g‘ri"
        )

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Siz muvaffaqiyatli tizimdan chiqdingiz.")
    return redirect("login")