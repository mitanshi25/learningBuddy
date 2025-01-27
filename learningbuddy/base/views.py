from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail

# from .models import OTP
from django.conf import settings
import random
# rooms = [ 
#     {'id' : 1 , 'name' : "'lets learn python"},
#     {'id' : 2 , 'name' : "lets learn java"},
#     {'id' : 3 , 'name' : "C++ full course"},
#     {'id' : 4 , 'name' : "build production level pipeline"},
    
# ]

# Create your views here.

# def loginPage(request):

#     page = "login"

#     if request.user.is_authenticated:
#         return redirect ('home')


#     if request.method =="POST":
#         username = request.POST.get('username').lower()
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'user does not exists')
        
#         user = authenticate(request, username=username,password=password)
#         if user is not None:
#             login(request, user)
#             return redirect ("home")
#         else:
#             messages.error(request, "username or password is not exist")

#     context = {'page':page}
#     return render (request, 'base/login_register.html', context)






otp_storage = {}  # Temporary storage for OTPs (use a database in production)

# def loginPage(request):
#     page = "login"

#     # Redirect if the user is already authenticated
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == "POST":
#         if 'username' in request.POST and 'password' in request.POST:
#             # Password-based login
#             username = request.POST.get('username').lower()
#             password = request.POST.get('password')

#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 messages.error(request, 'User does not exist')
#                 return redirect('login')

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, "Invalid username or password")

#         elif 'email' in request.POST:
#             # OTP-based login - Step 1: Send OTP
#             email = request.POST.get('email').lower()
#             try:
#                 user = User.objects.get(email=email)
#                 otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
#                 otp_storage[email] = otp  # Save OTP temporarily

#                 # Send OTP via email
#                 send_mail(
#                     'Your Login OTP',
#                     f'Your OTP for login is: {otp}',
#                     settings.DEFAULT_FROM_EMAIL,
#                     [email],
#                     fail_silently=False,
#                 )
#                 messages.success(request, 'OTP sent to your email')
#                 return redirect('login')  # Redirect back to the login page for OTP verification
#             except User.DoesNotExist:
#                 messages.error(request, 'Email does not exist')
#                 return redirect('login')

#         elif 'otp' in request.POST:
#             # OTP-based login - Step 2: Verify OTP
#             email = request.POST.get('email').lower()
#             otp = request.POST.get('otp')

#             if email in otp_storage and str(otp_storage[email]) == otp:
#                 try:
#                     user = User.objects.get(email=email)
#                     login(request, user)
#                     del otp_storage[email]  # Remove the OTP after successful login
#                     return redirect('home')
#                 except User.DoesNotExist:
#                     messages.error(request, 'User does not exist')
#             else:
#                 messages.error(request, 'Invalid OTP')

#     context = {'page': page}
#     return render(request, 'base/login_register1.html', context)

def loginPage(request):
    page = "login"

    # Redirect if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        action = request.POST.get('action', '')

        if action == "send_otp":
            # OTP-based login - Step 1: Send OTP
            email = request.POST.get('email').lower()
            try:
                user = User.objects.get(email=email)
                otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
                otp_storage[email] = otp  # Save OTP temporarily

                # Send OTP via email
                send_mail(
                    'Your Login OTP',
                    f'Your OTP for login is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email')
            except User.DoesNotExist:
                messages.error(request, 'Email does not exist')
            return redirect('login')  # Stay on the login page

        elif action == "verify_otp":
            # OTP-based login - Step 2: Verify OTP
            email = request.POST.get('email').lower()
            otp = request.POST.get('otp')

            if email in otp_storage and str(otp_storage[email]) == otp:
                try:
                    user = User.objects.get(email=email)
                    login(request, user)
                    del otp_storage[email]  # Remove the OTP after successful login
                    return redirect('home')
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist')
            else:
                messages.error(request, 'Invalid OTP')
            return redirect('login')  # Stay on the login page

        elif 'username' in request.POST and 'password' in request.POST:
            # Password-based login
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return redirect('login')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")

    context = {'page': page}
    return render(request, 'base/login_register1.html', context)



def logoutPage(request):
    logout(request)
    return redirect ('home')

# def registerUser(request):
#     page = 'register'
#     form = UserCreationForm()
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect ('home')
#         else:
#             messages.error(request,"an error occured during registration")
#     return render (request,'base/login_register.html',{'form':form})



def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration.")

    return render(request, 'base/login_register1.html', {'form': form, 'page': page})




def home (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q)|
                                Q(name__icontains=q) |
                                Q(description__icontains=q) |
                                Q(host__username__icontains=q) )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"rooms":rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages}
    return render (request , 'base/home.html', context)

def room (request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room= room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room', pk= room.id)
    context = {'room':room, 'room_messages':room_messages,'participants':participants}
    return render (request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user':user, 'rooms':rooms, "room_messages":room_messages,'topics':topics }
    return render (request, 'base/profile.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name= request.POST.get('name'),
            description = request.POST.get('description'),
        )
      
        return redirect ('home')
    context = {'form':form, 'topics':topics}
    return render (request, 'base/room_form.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)  # Fetch the room or return 404 if not found
    form = RoomForm(instance=room)  # Pass the room instance to the form
    topics = Topic.objects.all()
    if request.user != room.host :
        return HttpResponse ('you are not allowed here')
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        return redirect('home')  # Redirect to the home page after saving

    # topics = Topic.objects.all()
    # topics = Topic.objects.all()
    context = {'form': form,'topics':topics,'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom (request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host :
        return HttpResponse ('you are not allowed here')
    if request.method == "POST":
        room.delete()
        return redirect ('home')
    return render (request, 'base/delete.html', {'obj':room})


@login_required(login_url='/login')
def deleteMessage (request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user :
        return HttpResponse ('you are not allowed here')
    if request.method == "POST":
        message.delete()
        return redirect ('home')
    return render (request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser (request):
    user = request.user
    form = UserForm(instance= user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect ('profile', pk=user.id)

    return render (request,'base/update-user.html', {"form":form})


def topicsPage(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics":topics}
    return render (request, 'base/topics.html',context)


def activityPage(request):
    room_messages = Message.objects.all()
    return render (request, "base/activity.html",{"room_messages":room_messages})