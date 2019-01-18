from django.contrib import admin
from .models import Post, Image, Poll, Option, Vote, Comment, PinnedPost, PostUpdate, Event

# Register your models here.

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(PinnedPost)
admin.site.register(PostUpdate)
admin.site.register(Event)

