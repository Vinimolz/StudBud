from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
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
    
    context = {}
    return render(request, 'base/room_form.html', context)