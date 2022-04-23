from django.contrib import admin
from .models import Handle, Contest, Rank
# Register your models here.

class HandleAdmin(admin.ModelAdmin):
    list_display = ('email','isVerified','isActive','handle',)
    search_fields = ('email','isVerified','handle',)
    list_filter = ('isVerified','isActive')
    list_per_page = 50
    actions = ('make_active','make_inactive',)

    def make_active(self, request, queryset):
        queryset.update(isActive=True)
    
    def make_inactive(self, request, queryset):
        queryset.update(isActive=False)

class ContestAdmin(admin.ModelAdmin):
    list_display = ('id','name','date','isSend', 'isParsed', 'tryCount')
    search_fields = ('id','name','date','isSend', 'isParsed')
    list_filter = ('isSend','isParsed',)
    actions = ('make_send' , 'make_unsend')

    def make_send(self, request, queryset):
        queryset.update(isSend=True)
    
    def make_unsend(self, request, queryset):
        queryset.update(isSend=False)

admin.site.register(Contest, ContestAdmin)
admin.site.register(Handle, HandleAdmin)
admin.site.register(Rank)
