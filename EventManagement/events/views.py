from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from .models import Event
from django.contrib import messages
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def delete_expired_events():
    now = timezone.now()

    for event in Event.objects.all():
        event_start = datetime.combine(event.date, event.start_time)
        event_end = event_start + timedelta(hours=2)

        if now >= timezone.make_aware(event_end):
            event.delete()

# Register



def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please login.")
            return redirect('login')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "User registered successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')




#loing

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # 🔥 FIX
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_event')  # 🔥 FIX
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Home
def home(request):
    return render(request,'base.html')

# Book Event


@login_required(login_url='login')

def book_event(request):

    if request.method == "POST":

        # ✅ Max 3 events per user
        user_events_count = Event.objects.filter(created_by=request.user).count()
        if user_events_count >= 3:
            messages.error(request, "❌ You can book only 3 events!")
            return redirect('my_bookings')

        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        start_time_str = request.POST.get('start_time')

        # 🔥 Convert string → date & time
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        event_time = datetime.strptime(start_time_str, "%H:%M").time()

        new_start = datetime.combine(event_date, event_time)
        new_end = new_start + timedelta(hours=2)

        # ✅ Check overlap with ACCEPTED events only
        accepted_events = Event.objects.filter(
            date=event_date,
            status='Accepted'
        )

        for event in accepted_events:
            existing_start = datetime.combine(event.date, event.start_time)
            existing_end = existing_start + timedelta(hours=2)

            # 🔥 Overlap logic (correct)
            if new_start < existing_end and new_end > existing_start:
                messages.error(
                    request,
                    "⛔ This time slot is already booked (2 hour overlap)"
                )
                return redirect('book_event')

        # ✅ Create event
        Event.objects.create(
            title=title,
            description=description,
            date=event_date,
            start_time=event_time,
            created_by=request.user,
            status='Pending'
        )

        messages.success(
            request,
            "✅ Event booked successfully! Waiting for admin approval."
        )
        return redirect('my_bookings')

    return render(request, 'book_event.html')

# My bookings (user specific)


@login_required(login_url='login')



def my_bookings(request):
    events = Event.objects.filter(created_by=request.user).order_by('date','start_time')
    return render(request, 'my_bookings.html', {'events': events})




# All accepted events
def booked_events(request):
    delete_expired_events()
    events = Event.objects.filter(status='Accepted')
    return render(request,'booked_events.html', {'events':events})


# user editing
@login_required(login_url='login')

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        event.title = request.POST['title']
        event.description = request.POST['description']
        event.date = request.POST['date']
        event.start_time = request.POST['start_time']
        event.status = 'Pending'   # edit ke baad again admin approval
        event.save()
        messages.success(request, "Event updated successfully")
        return redirect('my_bookings')

    return render(request, 'edit_event.html', {'event': event})
