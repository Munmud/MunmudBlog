from django.contrib import admin
from .models import Category, Post, Comment, EmailSubscriber
from django.db.models import Count
import os
from django.conf import settings


# Register your models here.

from django.core.mail import get_connection, EmailMultiAlternatives
def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection( username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


# for configuration of Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'slug',)
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'email','body')
    search_fields = ('email',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','status',)
    search_fields = ('title','status',)
    list_filter = ('cat','status',)
    list_per_page = 50
    actions = ['approve', 'pending','sendMail']

    def approve(self, request, queryset):
        queryset.update(status='approaved')
    
    def pending(self, request, queryset):
        queryset.update(status='pending')
    
    def sendMail(self, request, queryset):
        popularPosts = Post.objects.annotate(num_items=Count('comments')).order_by('-visitorCount','-num_items')[:4]
        for obj in queryset:
            datatuple = []
            for x in EmailSubscriber.objects.all():
                if x.is_active:
                    email = x.email
                    mp = {}
                    mp['title'] = obj.title
                    mp['slug'] = obj.slug
                    mp['id'] = x.uuid
                    mp['domain'] = os.environ.get('ALLOWED_HOSTS').split(',')[1]
                    mp['desc'] = obj.content
                    mp['image'] = obj.image
                    mp['Popular_Posts'] = popularPosts
                    mp['MEDIA_URL'] = settings.MEDIA_URL

                    from django.template.loader import render_to_string
                    from django.utils.html import strip_tags

                    subject = "Moontasir's Blog"
                    html_message = render_to_string('mail/newPost.html', mp)
                    plain_message = strip_tags(html_message)
                    from_email = "Moontasir's New Post <" + str(os.environ.get('EMAIL_HOST_USER')) + '>'
                    tple = (subject,plain_message,html_message,from_email,[email])
                    datatuple.append(tple)
            
            send_mass_html_mail(datatuple,)
            break


class EmailSubscriberAdmin(admin.ModelAdmin):
    model = EmailSubscriber
    fields = ['email', 'is_active']
    list_display = ('email','is_active',)
    list_per_page = 50
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active = True)
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active = False)


admin.site.register(Category, CategoryAdmin)
admin.site.register(EmailSubscriber, EmailSubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)