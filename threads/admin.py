from django.contrib import admin
from .models import Thread, Comment


class CommentInline(admin.TabularInline):  # adding an extra comment viewable option in our admin page
    model = Comment
    extra=0


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment)