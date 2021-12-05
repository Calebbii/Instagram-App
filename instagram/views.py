from django.contrib.auth.models import User
from django.shortcuts import render,redirect, get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from instagram.forms import CommentsForm,PostForm, Registration, UpdateProfile, UpdateUser
from instagram.models import Follows, Image, Likes, Profile
from django.contrib import messages

# Create your views here.
def home(request):
    comment_form = CommentsForm()
    post_form = PostForm()
    images = Image.display_images()
    all_users = User.objects.all()
    return render(request, 'home.html',{"images":images,"comment_form":comment_form,"post":post_form,"all_users":all_users})


def post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES) 
        if post_form.is_valid():
            the_post = post_form.save(commit = False)
            the_post.user = request.user
            the_post.save()
        return redirect('home')
    else:
        post_form = PostForm()
    return render(request,'post.html',{"post_form":post_form})

def detail(request,image_id):
    current_user = request.user
    try:
        image = get_object_or_404(Image, pk = image_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request, 'imageDetails.html', {'image':image,'current_user':current_user})

def search_results(request):
    if 'search_user' in request.GET and request.GET["search_user"]:
        search_term = request.GET.get('search_user')
        users = Profile.search_profiles(search_term)
        images = Image.search_photos(search_term)
        return render(request,'search.html',{"users":users,"images":images})
    else:
        return render(request,'search.html')

def register(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            username = form.cleaned_data.get('username')

            messages.success(request,f'Account for {username} created,you can now login')
        return redirect('login')
    else:
        form = Registration()
    return render(request,'registration/registration_form.html',{"form":form})


def profile(request):
    comment_form = CommentsForm()
    current_user = request.user
    images = Image.objects.all().order_by('-pub_date')
    all_users = User.objects.all()
    user_images = Image.objects.filter(user_id = current_user.id).all()
    
    return render(request,'profile.html',{"images":images,'all_users':all_users,'comment_form':comment_form,'user_images':user_images,"current_user":current_user})

 

def allcomments(request,photo_id):
    image = Image.objects.filter(pk = photo_id).first()
    return render(request,'comments.html',{"image":image})


def users_profile(request,pk):
    comment_form = CommentsForm()
    user = User.objects.get(id = pk)
    image = Image.objects.filter(user = user)
    c_user = request.user
    return render(request,'users_profile.html',{"user":user,'comment_form':comment_form,"image":image,"c_user":c_user})

def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUser(request.POST,instance=request.user)
        profile_form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Profile account has been updated successfully')
        return redirect('profile')
    else:
        user_form = UpdateUser(instance=request.user)
        profile_form = UpdateProfile(instance=request.user.profile) 
    params = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request,'update.html',params)

def follow(request,user_id):
    followee = request.user
    followed = Follows.objects.get(pk=user_id)
    follow_data,created = Follows.objects.get_or_create(follower = followee,followee = followed)
    follow_data.save()
    return redirect('others_profile')

def like(request, image_id):
    current_user = request.user
    image=Image.objects.get(id=image_id)
    new_like,created= Likes.objects.get_or_create(liker=current_user, image=image)
    new_like.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def unfollow(request,user_id):
    followee = request.user
    follower = Follows.objects.get(pk=user_id)
    follow_data = Follows.objects.filter(follower = follower,followee = followee).first()
    follow_data.delete()
    return redirect('users_profile')


def delete(request,photo_id):
    current_user = request.user
    photo = Image.objects.get(pk=photo_id)
    if photo:
        photo.delete_post()
    return redirect('home')


def commentFunction(request,photo_id):
    c_form = CommentsForm()
    photo = Image.objects.filter(pk = photo_id).first()
    if request.method == 'POST':
        c_form = CommentsForm(request.POST)
        if c_form.is_valid():
            comment = c_form.save(commit = False)
            comment.user = request.user
            comment.photo = photo
            comment.save() 
    return redirect('home')