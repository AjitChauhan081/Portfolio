from django.contrib import admin
from .models import Blog,BlogPost,Category,Comment

admin.site.register(Blog)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Comment)
