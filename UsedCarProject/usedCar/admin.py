from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import UserProfile, PostSell, PostSellImages, LikePost, Follow, Thread, ChatMessage

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PostSell)
admin.site.register(PostSellImages)
admin.site.register(LikePost)
admin.site.register(Follow)
admin.site.register(ChatMessage)

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread

admin.site.register(Thread, ThreadAdmin)
