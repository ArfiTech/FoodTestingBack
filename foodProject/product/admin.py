from django.contrib import admin
from .models import Question

from .models import Customer
# from .models import Market
# from .models import Post
# from .models import Review
# from .models import ReviewHash
# from .models import Hashtag

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Customer)
# admin.site.register(Market)
# admin.site.register(Post)
# admin.site.register(Review)
# admin.site.register(ReviewHash)
# admin.site.register(Hashtag)
