from django.conf.urls import url
from django.urls.conf import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',views.home,name = 'home'),
    path('image/<int:image_id>',views.detail,  name='photo.detail'),
    path('profile/',views.profile,name='profile'),
    path('post/',views.post_image,name='post'),
    path('search/',views.search_results,name='search'),
    path('comment/<int:image_id>',views.comment,name='comment'),
    path('update/',views.profile_update,name='profile_update'),
    path('userprofile/',views.users_profile,name='users_profile'),
    path('accounts/register/',views.register,name='register'),
    path('',auth_views.LoginView.as_view(template_name = 'registration/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'registration/logout.html'),name='logout'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)