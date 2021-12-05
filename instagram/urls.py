from django.conf.urls import url
from django.urls.conf import path,re_path
from . import views
from . import views as app_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.home,name = 'home'),
    path('search/',views.search_results,name='search'),
    path('userprofile/',views.users_profile,name='users_profile'),
    path('accounts/register/',app_views.register,name='register'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)