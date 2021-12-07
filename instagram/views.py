from django.contrib.auth.models import User
from django.shortcuts import render,redirect, get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from instagram.forms import CommentsForm,PostForm, Registration, UpdateProfile, UpdateUser
from instagram.models import Follows, Image, Likes, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    comment_form = CommentsForm()
    post_form = PostForm()
    images = Image.display_images()
    all_users = User.objects.all()
    base_image = "https://res.cloudinary.com/dtbko4o5h/image/upload/v1638685260/"
    return render(request, 'home.html',{"images":images,"comment_form":comment_form,"post":post_form,"base_image":base_image,"all_users":all_users})

@login_required(login_url='/accounts/login/')
def post_image(request):
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

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'search_user' in request.GET and request.GET["search_user"]:
        search_term = request.GET.get('search_user')
        users = Profile.search_profiles(search_term)
        images = Image.search_images(search_term)
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

@login_required(login_url='/accounts/login/')
def profile(request):
    comment_form = CommentsForm()
    current_user = request.user
    images = Image.objects.all().order_by('-pub_date')
    all_users = User.objects.all()
    user_images = Image.objects.filter(user_id = current_user.id).all()
    
    return render(request,'profile.html',{"images":images,'all_users':all_users,'comment_form':comment_form,'user_images':user_images,"current_user":current_user})

@login_required(login_url='/accounts/login/')
def users_profile(request,pk):
    comment_form = CommentsForm()
    user = User.objects.get(id = pk)
    image = Image.objects.filter(user = user)
    c_user = request.user
    return render(request,'users_profile.html',{"user":user,'comment_form':comment_form,"image":image,"c_user":c_user})

@login_required(login_url='/accounts/login/')
def profile_update(request):
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
    return render(request,'update_profile.html',params)

@login_required(login_url='/accounts/login/')
def delete(request,image_id):
    current_user = request.user
    image = Image.objects.get(pk=image_id)
    if image:
        image.delete_post()
    return redirect('home')


@login_required(login_url='/accounts/login/')
def comment(request,image_id):
    current_user = request.user
    image = Image.get_single_image(id=image_id)
    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)
       
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = current_user
            comment.image_id = image_id
            comment.save()
        return redirect('/')

    else:
        comment_form = CommentsForm()
        return render(request,'comment.html',{"comment_form":comment_form,"image":image})  

@login_required(login_url='/accounts/login/')
def allcomments(request,image_id):
    image = Image.objects.filter(pk = image_id).first()
    return render(request,'comments.html',{"image":image})

@login_required(login_url='/accounts/login/')
def follow(request,user_id):
    followee = request.user
    followed = Follows.objects.get(pk=user_id)
    follow_data,created = Follows.objects.get_or_create(follower = followee,followee = followed)
    follow_data.save()
    return redirect('others_profile')

# def like(request, image_id):
#     current_user = request.user
#     image=Image.objects.get(id=image_id)
#     new_like,created= Likes.objects.get_or_create(liker=current_user, image=image)
#     new_like.save()

#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


def image_likes(request,image_id):
    image =  Image.get_single_image(image_id)
    user = request.user
    user_id = user.id
    
    if user.is_authenticated:
    
        image.save()
        
    return redirect('home')

@login_required(login_url='/accounts/login/')
def unfollow(request,user_id):
    followee = request.user
    follower = Follows.objects.get(pk=user_id)
    follow_data = Follows.objects.filter(follower = follower,followee = followee).first()
    follow_data.delete()
    return redirect('users_profile')