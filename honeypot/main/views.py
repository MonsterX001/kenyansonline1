from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Houseuploads, Shots, User, Views, Comment, FollowersCount, Share
from .filters import ListingFilter
from django.core.paginator import Paginator
from django.urls import reverse
import uuid
from .helpers import send_forgetpassword_mail
from django.db.models import Q
from itertools import chain
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required(login_url='/signin')
def index(request):
    user_profile = Profile.objects.filter(user=request.user)
    listings = Houseuploads.objects.all()
    user_posts = Houseuploads.objects.filter(user=request.user)
    listing_filter = ListingFilter(request.GET, queryset = listings)
    
    #set pagination
    #X = user_posts()

    p = Paginator(Houseuploads.objects.all(), 9)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context ={
        'listing_filter': listing_filter,
        'listings': listings,
        'venues' : venues,
        'user_profile' :user_profile,
        'user_post' :user_posts,
    }

    return render(request, 'index.html',  context)

@login_required(login_url='/signin')
def Recommended(request):
    user_following_list = []
    feed = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Houseuploads.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))
    context ={
        'feed_list':feed_list,
        'user_following':user_following_list
    }

    return render(request, 'recommended.html',  context)


def trending_posts(request):
    # Calculate the date one week ago
    one_week_ago = timezone.now() - timedelta(weeks=1)

    # Fetch the trending posts based on views in the last week
    trending_posts = Houseuploads.objects.filter(created_at__gte=one_week_ago).order_by('-no_of_views')[:10]

    return render(request, 'trending.html', {'trending_posts': trending_posts})

@login_required(login_url='/signin')
def share_view(request):
    if request.method == 'POST':
        user = request.user
        shared_link = request.POST['shared_link']
        Share.objects.create(user=user, shared_link=shared_link)
        # Redirect to a success page or the shared link's page
        return redirect('success-page')

    # Handle GET requests or render the share form
    return render(request, 'base.html')

def share_view(request):
    # Retrieve the Share object
    share = Share.objects.first()

    # Increment the share_count
    share.share_count += 1
    share.save()
    context = {
        'share_count': share.share_count,
    }
    # Redirect the user to the desired page after sharing
    
    return render(request, 'target_page.html', context)

@login_required(login_url='/signin')
def link_detail_view(request, link_id):
    shared_link = Share.objects.filter(user=request.user, shared_link=link_id).count()
    context = {'shared_link': shared_link}
    return render(request, 'account.html', context)

@login_required(login_url='/signin')
def shotss(request):
 
        #user_profile = Profile.objects.get(user=request.user)
        listings = Shots.objects.all()
        user_posts = Shots.objects.filter(user=request.user)
        listing_filter = ListingFilter(request.GET, queryset = listings)
        
        #set pagination
        #X = user_posts()

        p = Paginator(Shots.objects.all(), 20)
        page = request.GET.get('page')
        venues = p.get_page(page)

        context ={
            'listing_filter': listing_filter,
            'listings': listings,
            'venues' : venues,
            #'user_profile' :user_profile,
            'user_post' :user_posts,
        }

        return render(request, 'shotvideos.html',  context)

@login_required(login_url='/signin')
def hookup(request):
    user_profile = Profile.objects.filter(user=request.user)
    user_profiles = Profile.objects.all()
    context ={
        'user_profiles':user_profiles,
        'user_profile':user_profile,
    }

    return render(request, 'hookups.html', context)

def socialbook(request, agentname):
    profile = get_object_or_404(Profile, agentname=agentname)
    user_object = User.objects.get(username=agentname)
    user_profile = Profile.objects.get(user=user_object)
   
    
    context ={
        'user_profile':user_profile,
        'profile':profile,
    }

    return render(request, 'socialbook.html', context)

@login_required(login_url='/signin')
def livechat(request):
    
    return render(request, 'livechat.html')
def terms_policy(request):
    
    return render(request, 'termspolicy.html')

@login_required(login_url='/signin')   
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        videos = Houseuploads.objects.filter( Q(details__contains=searched)| Q(user__contains=searched)| Q(Video_name__contains=searched))

        context ={
            'videos': videos
        }

    return render(request, 'searches.html', context)

@login_required(login_url='/signin')   
def profilesearch(request):
    if request.method == "POST":
        searched = request.POST['searched']
        profile = Profile.objects.filter( Q(agentname__contains=searched) | Q(location__contains=searched) | Q(bio__contains=searched))
        context ={
                    'profile': profile
                }
        if profile != 0:
            return render(request, 'profile_searches.html', context)
           
        elif profile==0:
            messages.info(request, 'your search was not found, try another way')     
            return redirect( '/profile-search')
        else:
            messages.info(request, 'your search was not found, try another way')     
            return redirect( '/profile-search')
    else:
        return render(request, 'profile_searches.html')
        
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user and redirect to uploading page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login) 
                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect ('/acc-profile')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('/register')
    else:
        return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Are Invalid')
            return redirect('/signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='/signin')
def account(request, pk):
   
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Houseuploads.objects.filter(user=pk)
    user_post = Shots.objects.filter(user=pk)
    user_followers = len(FollowersCount.objects.filter(user=pk))

    calculated_values = []
    for x in user_posts:
        y=x.no_of_views
        z=y*0.3

        calculated_values.append(z)

    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post':user_post,
        'calculated_values':calculated_values,
        'user_followers':user_followers
    }


    return render(request, 'account.html', context)

@login_required(login_url='/signin')
def podcast(request):
    user_profile = Profile.objects.filter(user=request.user)
    listings = Houseuploads.objects.all()
    user_posts = Houseuploads.objects.filter(user=request.user)
    listing_filter = ListingFilter(request.GET, queryset = listings)
    
    #set pagination
    #X = user_posts()

    p = Paginator(Houseuploads.objects.all(), 9)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context ={
        'listing_filter': listing_filter,
        'listings': listings,
        'venues' : venues,
        'user_profile' :user_profile,
        'user_post' :user_posts,
    }

    return render(request, 'podcast.html',  context)

@login_required(login_url='/signin')
def blog(request):
    user_profile = Profile.objects.filter(user=request.user)
    listings = Houseuploads.objects.all()
    user_posts = Houseuploads.objects.filter(user=request.user)
    listing_filter = ListingFilter(request.GET, queryset = listings)
    
    #set pagination
    #X = user_posts()

    p = Paginator(Houseuploads.objects.all(), 9)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context ={
        'listing_filter': listing_filter,
        'listings': listings,
        'venues' : venues,
        'user_profile' :user_profile,
        'user_post' :user_posts,
    }

    return render(request, 'blog.html',  context)

@login_required(login_url='/signin')
def acc(request):
    user_posts = Houseuploads.objects.filter(user=request.user)
    user_profile = Profile.objects.get(user=request.user)
        
    context={
        'user_posts':user_posts,
        'user_profile': user_profile,
    }
    
    if request.method == 'POST' and 'profile_submit' in request.POST:
        if request.FILES.get('image') == None:
            profileimg = user_profile.profileimg
            agentname = request.POST['agencyname']
            location = request.POST['location']
            bio =request.POST['agentdetails']

            user_profile.profileimg = profileimg
            user_profile.agentname = agentname
            user_profile.location = location
            user_profile.bio = bio 
                   
            user_profile.save()
            return redirect('/acc-profile')
            
        elif request.FILES.get('image') != None:

            profileimg = request.FILES.get('image')
            agentname = request.POST['agencyname']
            location = request.POST['location']
            bio =request.POST['agentdetails']

            user_profile.profileimg = profileimg
            user_profile.agentname = agentname
            user_profile.location = location
            user_profile.bio = bio 
            user_profile.save()      

            return redirect('/acc-profile')

    else: 
        user_profile.refresh_from_db()      
        

        return render(request, 'acc-profile.html', context)


@login_required(login_url='/signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Houseuploads.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'UNSUBSCRIBE'

    else:
        button_text = 'SUBSCRIBE'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers': user_followers,

    }
    return render(request, 'profile.html', context)
    


@login_required(login_url='/signin')
def Houseupload(request):

    if request.method == 'POST':
        
        user = request.user.username
        video_name = request.POST['housename']
        main_img = request.FILES.get('mainimg')
        details = request.POST['details']
        
        new_post =  Houseuploads.objects.create(user = user, Video_name=video_name, main_img=main_img, details=details) 
        new_post.save() 
        return redirect('/acc-profile')
    
    
    return render(request, 'houseuploads.html',)
@login_required(login_url='/signin')
def Shot(request):

    if request.method == 'POST':
        
        user = request.user.username
        video_name = request.POST['housename']
        main_img = request.FILES.get('mainimg')
        details = request.POST['details']


        new_post =  Shots.objects.create(user = user, Video_name=video_name, main_img=main_img, details=details) 
        new_post.save()
        return redirect('/acc-profile')
    
    
    return render(request, 'shots.html',)
@login_required(login_url='/signin')
def video_play(request, id):
   
    posts = Houseuploads.objects.filter(id = id)
    video = get_object_or_404(Houseuploads, pk=id)
    comments = Comment.objects.filter(video=video)
    

    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment(user=request.user, video=video, text=text)
        comment.save()

    user_post_length = len(comments)

    
    videos = Houseuploads.objects.get(id=id)
    related_videos = Houseuploads.objects.filter(details__contains=videos.details).exclude(id=id)[:5]  # Example: get videos with similar titles, excluding the current video

    context={
        'posts':posts,
        'video': video,
        'video': videos,
        'comments': comments,
        'user_post_length': user_post_length,
        'related_videos': related_videos
    }
    username = request.user.username


    post = Houseuploads.objects.get( id = id)

    like_filter = Views.objects.filter(post_Id=id, username=username).first()

    if like_filter == None:
        new_view = Views.objects.create(post_Id=id, username=username)
        new_view.save()
        post.no_of_views = post.no_of_views + 1
        post.save()
    else:
        post.no_of_views = post.no_of_views 
        post.save()     
    return render(request, 'video_play.html', context)


def changepassword(request , token):
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_pasword = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'user id not found')
                return redirect('/changepassword/{token}')

            if new_password != confirm_pasword:
                messages.success(request, 'Passwords not matching')
                return redirect('/changepassword/{token}')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save
            return redirect('/signin')
        
        #context={'user_id' : profile_obj.user.id}

    except Exception as e:
        print(e)
    return render(request, 'changepassword.html')


def forgotpassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('username')

            if not User.objects.filter(email=email).first():
                messages.success(request, 'That email adress does not exist')
                return redirect('/forgotpassword')

            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()

            send_forgetpassword_mail(user_obj.email, token)
            messages.success(request, 'An Email has been sent, click on the link to reset password')
            return redirect('/forgotpassword')

    except Exception as e:
        print(e)    
    return render(request, 'forgotpassword.html')

@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect ('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
    
