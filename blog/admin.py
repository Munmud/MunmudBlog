from django.contrib import admin
from .models import Category, Post, Comment, EmailSubscriber


# Register your models here.

# for configuration of Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'slug',)
    search_fields = ('title',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','add_date',)
    search_fields = ('title',)
    list_filter = ('cat',)
    list_per_page = 50

class EmailSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email','is_active',)
    list_per_page = 50



admin.site.register(Category, CategoryAdmin)
admin.site.register(EmailSubscriber, EmailSubscriberAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)