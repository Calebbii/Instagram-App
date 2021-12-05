from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comments,Image
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ['image','image_name','image_caption']

class CommentsForm(forms.ModelForm):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.fields['comment'].widget=forms.TextInput()
    self.fields['comment'].widget.attrs['placeholder']='Leave a comment...'
  class Meta:
    model = Comments
    fields = ('comment',)
    
class Registration(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username','email','password1','password2']

class UpdateProfile(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['profile_image','bio']

class UpdateUser(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username','email']
