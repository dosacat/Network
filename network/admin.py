from django.contrib import admin
from .models import Profile, User,NetworkPost,Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)

class MyModelAdmin(admin.ModelAdmin):
     readonly_fields= ['timestamp',]
admin.site.register(NetworkPost, MyModelAdmin)