from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Profile, Post, Reel, Message, Comment, Notification, Like
from django.http import JsonResponse

# ---------- AUTH ----------


@login_required
def settings_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')

        # Update User model
        if username:
            request.user.username = username
        if email:
            request.user.email = email
        request.user.save()

        # Update Profile model
        if dob:
            profile.dob = dob
        if mobile:
            profile.mobile = mobile
        if gender:
            profile.gender = gender
        if profile_pic:
            profile.profile_pic = profile_pic

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('settings')  # change to your URL name

    context = {
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'note/settings.html', context)


def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'note/notifications.html', {'notifications': notifications})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        userid = request.POST.get("userid").strip()   # assuming this is the username
        dob = request.POST.get("dob")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        profile_pic = request.FILES.get("profile_pic")

        # Validation
        if not username or not userid or not password or not confirm:
            messages.error(request, "All fields are required!")
            return redirect("register")

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=userid).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        # Create User
        user = User.objects.create_user(username=userid, first_name=username, password=password)
        user.save()

        # Create Profile linked to User
        profile = Profile.objects.create(
            user=user,
            dob=dob,
            mobile=mobile,
            gender=gender,
            profile_pic=profile_pic
        )
        profile.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")  # replace with your login URL name

    return render(request, "note/register.html")




def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'note/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- HOME ----------

@login_required(login_url='login')



def home_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'note/home.html', {'posts': posts})

def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('home')

def add_comment(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        post = Post.objects.get(id=post_id)
        Comment.objects.create(post=post, user=request.user, text=text)
    return redirect('home')


# ---------- PROFILE ----------

@login_required(login_url='login')
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')
    reels = Reel.objects.filter(user=user_profile).order_by('-created_at')
    profile = Profile.objects.get(user=user_profile)
    return render(request, 'note/profile.html', {
        'user_profile': user_profile,
        'posts': posts,
        'reels': reels,
        'profile': profile
    })


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', profile.bio)
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile', username=request.user.username)
    return render(request, 'note/edit_profile.html', {'profile': profile})


# ---------- POSTS + REELS ----------

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        if image:
            Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('home')
    return render(request, 'note/create_post.html')




@login_required
def reels_view(request):
    reels = Reel.objects.all().order_by('-created_at')
    return render(request, 'note/reels.html', {'reels': reels})

@login_required
def add_comment(request, reel_id):
    if request.method == 'POST':
        reel = get_object_or_404(Reel, id=reel_id)
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(reel=reel, user=request.user, text=text)
    return redirect('reels')

@login_required
def toggle_like(request, reel_id):
    if request.method == 'POST':
        reel = get_object_or_404(Reel, id=reel_id)
        like, created = Like.objects.get_or_create(reel=reel, user=request.user)
        if not created:
            # user already liked, so remove like
            like.delete()
            liked = False
        else:
            liked = True
        # return JSON response for AJAX
        return JsonResponse({'liked': liked, 'total_likes': reel.like_set.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)



# ---------- MESSAGES ----------

@login_required(login_url='login')
def messages_view(request, username):
    other_user = get_object_or_404(User, username=username)
    msgs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text.strip():
            Message.objects.create(sender=request.user, receiver=other_user, text=text)
            return redirect('messages', username=username)

    return render(request, 'note/messages.html', {
        'msgs': msgs,
        'other_user': other_user
    })


# ---------- SEARCH ----------

@login_required(login_url='login')
def search_view(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query)
    return render(request, 'note/search.html', {'results': results, 'query': query})
