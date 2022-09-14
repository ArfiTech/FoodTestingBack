from django.contrib import admin

# Register your models here.
from .models import Customer
from .models import Market
from .models import Post
from .models import Review

admin.site.register(Customer)
admin.site.register(Market)
admin.site.register(Post)
admin.site.register(Review)