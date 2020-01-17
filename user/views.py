from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegister


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created For {username}')

            return redirect('home')
    else:
        form = UserRegister()

    return render(request, 'register.html', {'form': form})
