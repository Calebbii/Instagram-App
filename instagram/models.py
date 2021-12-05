from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images', blank =True, null = True)
    image_name = models.CharField(max_length=60)
    image_caption = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def save_image(self):
        self.save()

    @classmethod
    def display_images(cls):
        photos = cls.objects.all().order_by('-pub_date')
        return photos

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
    profile_image = models.ImageField(upload_to = 'images/', blank=True, null=True)
    bio = models.TextField()
    user = models.OneToOneField(User,on_delete = models.CASCADE)

    @classmethod
    def search_profiles(cls,search_term):
        profiles = cls.objects.filter(user__username__icontains = search_term).all()
        return profiles
class Comments(models.Model):
    comment = models.CharField(max_length = 50, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')

class Likes(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE,related_name='photolikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liker = models.ForeignKey(User,on_delete = models.CASCADE,related_name='userlikes')


class Follows(models.Model):
    follower = models.ForeignKey(Profile, related_name='following',on_delete = models.CASCADE)
    followee = models.ForeignKey(Profile, related_name='followers',on_delete = models.CASCADE)