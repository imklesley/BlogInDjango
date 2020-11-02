from django.contrib import admin
from blog.models import BlogPost

# Referencia no admin para poder realizar operações no bd com interface do próprio django
admin.site.register(BlogPost)
