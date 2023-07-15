from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.
"""
rooms = [
    {'id': 1, 'name': 'Learn Python'},
    {'id': 2, 'name': 'Learn Java'},
    {'id': 3, 'name': 'Learn C/C++'},
]
"""

def login_page(request):

    page_name = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    
    context = {'page_name': page_name}
    return render(request, 'base/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    page_name = 'register'

    form = UserCreationForm()    

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')        
            else:
                print('ERROR MESSAGE HERE -------------------')
                messages.error(request, 'An error has occurred during registration')
        except Exception as e:
            messages.error(request, 'An error has occurred during registration')
            print(f'Error occured in registration. ERROR: {str(e)}')

    context = {'page_name': page_name, 'form': form}

    return render(request, 'base/login_register.html', context)



def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )

    room_count = rooms.count()

    topics = Topic.objects.all()

    content = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', content)

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    content = {'room': room}
    return render(request, 'base/room.html', content)

@login_required(login_url='login')
def create_room(request):

    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete_form.html', {'obj': room})