from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import BlogHome, BlogPost, CategoryView, searchPost, emailSubscription, unsubscribeEmail

# app_name = 'blog'
urlpatterns = [
    path('', BlogHome, name='home'),
    path('blog/<slug:slug>/', BlogPost, name='single_post'),
    path('category/<slug:slug>/', CategoryView, name='Category'),
    path('search/', searchPost, name='searchPost'),
    path('emailSubscription/', emailSubscription, name='emailSubscription'),
    path('unsubscribeEmail/<str:pk>',unsubscribeEmail,name='unsubscribeEmail'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)