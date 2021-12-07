from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images', blank =True, null = True)
    image_name = models.CharField(max_length=200)
    image_caption = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete = models.CASCADE)

    def save_image(self):
        self.save()

    @classmethod
    def display_images(cls):
        photos = cls.objects.all().order_by('-pub_date')
        return photos
    @classmethod
    def get_single_image(cls,id):
        image = cls.objects.get(pk=id)
        return image

    @property
    def saved_comments(self):
        return self.comments.all()

    @property
    def saved_likes(self):
        return self.imagelikes.count()

    @classmethod
    def search_images(cls,search_term):
        images = cls.objects.filter(image_name__icontains = search_term).all()
        return images

    def delete_post(self):
        self.delete()

    def __str__(self):
        return "%s image" % self.image_name

class Profile(models.Model):
    profile_image = models.ImageField(upload_to = 'images', blank=True, null=True)
    bio = models.TextField()
    user = models.OneToOneField(User,on_delete = models.CASCADE)


    def create_profile(instance,sender,created,**kwargs):
        if created:
            Profile.objects.create(user = instance)


    def save_profile(sender,instance,**kwargs):
        instance.profile.save()

    @property
    def saved_followers(self):
        return self.followers.count()   

    @property
    def saved_following(self):
        return self.following.count() 


    @property
    def follows(self):
        return [follow.followee for follow in self.following.all()]

    @property
    def following(self):
        return self.followers.all()

    @classmethod
    def search_profiles(cls,search_term):
        profiles = cls.objects.filter(user__username__icontains = search_term).all()
        return profiles

    def __str__(self):
        return "%s profile" % self.user

class Comments(models.Model):
    comment = models.CharField(max_length = 50, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')

    @classmethod
    def display_comments_by_image_Id(cls,image_id):
        comments = cls.objects.filter(image_id = image_id)
        return comments

    def __str__(self):
        return "%s comment" % self.image



class Likes(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='photolikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liker = models.ForeignKey(User,on_delete = models.CASCADE,related_name='userlikes')

    def __str__(self):
        return "%s like" % self.image

class Follows(models.Model):
    follower = models.ForeignKey(Profile, related_name='following',on_delete = models.CASCADE)
    followee = models.ForeignKey(Profile, related_name='followers',on_delete = models.CASCADE)

    def __str__(self):
        return "%s follower" % self.follower