from django.contrib import admin
from .models import Category, Post, Comment, EmailSubscriber,Image
from django.db.models import Count
import os
from django.conf import settings
from codeforces.helper import send_mass_html_mail


# Register your models here.

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

class ImageAdmin(admin.ModelAdmin):
    fields = ['image', 'imageAltText']
    list_display = ( 'admin_photo', 'imageAltText')
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(EmailSubscriber, EmailSubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)