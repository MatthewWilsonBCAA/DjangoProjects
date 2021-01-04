# from django.contrib import admin
# from .models import Post

# # Register your models here.
# admin.site.register(Post)
from django.contrib import admin
from .models import Post, Comment


class CommentInLine(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)