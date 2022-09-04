from django.db import models

# Create your models here.
from django.db import models
'''
class Product(models.Model):
    name = models.CharField(max_length=70)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
'''

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

class Customer(models.Model):
    UUID = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    nickname = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    profile_photo = models.CharField(max_length=30)
    age = models.IntegerField()
    birthday = models.DateField()
    #phone_num = models.IntegerField()
    is_social = models.BooleanField()

class Product(models.Model):
    name = models.CharField(max_length=70)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

'''
class Market(models.Model):
    business_reg_num = models.CharField(max_length=30)
    reg_date = models.DateField()
    due_time = models.DateField()
    customer_UUID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    review_PW = models.IntegerField()
    #hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

class Post(models.Model):
    UUID = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=30)
    market = models.ForeignKey(Market, on_delta=models.CASCADE)
    post_date = models.DateField()
    last_update = models.DateField()
    photo = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    #context =
    writer = models.CharField(max_length=30)
    price = models.IntegerField()
    #test_price =
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    origin = models.CharField(max_length=30)

class Review(models.Model):
    UUID = models.UUIDField(primary_key=True)
    writer = models.CharField(max_length=30)
    photo = models.CharField(max_length=30)
    review_date = models.DateField()

class Hashtag(models.Model):
    name = models.CharField(max_length=30)
    is_good = models.BooleanField()

class ReviewHash(models.Model):
    reviewer_UUID = models.ForeignKey(Review, on_delta=models.CASCADE)
    hashtag_name = models.ForeignKey(Hashtag, on_delta=models.CASCADE)
    mention_num = models.IntegerField()
    market_name = models.ForeignKey(Market, on_delta=models.CASCADE)
'''