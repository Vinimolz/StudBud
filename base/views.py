from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
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
    return redirect('login')

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

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    topics = Topic.objects.all()[0:5]

    content = {'rooms': rooms,
                'topics': topics,
                'room_count': room_count,
                'room_messages': room_messages}
    
    return render(request, 'base/home.html', content)

def room(request, pk):
    room = Room.objects.get(id=pk)
    user_messages = room.message_set.all()

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    content = {'room': room, 'user_messages': user_messages, 'participants': participants}
    return render(request, 'base/room.html', content)

@login_required(login_url='login')
def create_room(request):

    form = RoomForm()

    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )

        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user,
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics}
    
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def update_room(request, pk):

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')

        room.save()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}

    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete_form.html', {'obj': room})

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('This actions is not allowed')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete_form.html', {'obj': message})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            print('invalid form')

    return render(request, 'base/update_user.html', {'form': form})

def topics_page(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics.html', {'topics': topics})