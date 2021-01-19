from django.contrib import admin
from .models import Post, Post_Likes, User_Following

# Register your models here.
admin.site.register(Post)
admin.site.register(Post_Likes)
admin.site.register(User_Following)