from django.contrib import admin
from .models import House, Profile, Comment, Evaluation

# Register your models here.
admin.site.register(House)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Evaluation)
