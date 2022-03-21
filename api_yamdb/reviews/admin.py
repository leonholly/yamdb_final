from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'title', 'author', 'text', 'score')
    search_fields = ('text',)
    list_filter = ('title', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'review', 'author', 'text')
    search_fields = ('text',)
    list_filter = ('review', 'author')


admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
