# from django.contrib import admin
# from .models import Post

# # Register your models here.
# admin.site.register(Post)
from django.contrib import admin
from .models import Post, Comment, Vote, Follow


class VoteDisplay(admin.StackedInline):
    model = Vote
    extra = 0


class CommentInLine(admin.StackedInline):
    model = Comment
    extra = 0


class FollowInLine(admin.StackedInline):
    model = Follow
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
        VoteDisplay,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Follow)