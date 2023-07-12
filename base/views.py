from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Create your views here.
"""
rooms = [
    {'id': 1, 'name': 'Learn Python'},
    {'id': 2, 'name': 'Learn Java'},
    {'id': 3, 'name': 'Learn C/C++'},
]
"""

def home(request):
    rooms = Room.objects.all()
    content = {'rooms': rooms}
    return render(request, 'base/home.html', content)

def room(request, pk):
    room = Room.objects.get(id=pk)
    
    content = {'room': room}
    return render(request, 'base/room.html', content)

def create_room(request):

    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method== 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)