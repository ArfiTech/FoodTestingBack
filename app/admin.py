from django.contrib import admin

# Register your models here.
from .models import Customer, Market, Post, Quesbymarket, Questionlist, Review, DropBox

admin.site.register(Customer)
admin.site.register(Market)
admin.site.register(Post)
admin.site.register(Quesbymarket)
admin.site.register(Questionlist)
admin.site.register(Review)
admin.site.register(DropBox)
