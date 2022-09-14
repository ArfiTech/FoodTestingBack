from django.db import models

# Create your models here.


class Customer(models.Model):
    uuid = models.CharField(primary_key=True, max_length=36)
    password = models.CharField(max_length=15)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=17, blank=True, null=True)
    nickname = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=1)
    profile_photo = models.TextField(blank=True, null=True)
    born_date = models.CharField(max_length=10, blank=True, null=True)
    customer_type = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'customer'


class Market(models.Model):
    reg_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    menu_photo = models.TextField()
    start_date = models.BigIntegerField()
    customer_uuid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customer_uuid')
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    phone_num = models.CharField(max_length=13)
    category = models.CharField(max_length=10)
    hashtag = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'market'


class Post(models.Model):
    post_uuid = models.CharField(primary_key=True, max_length=36)
    subject = models.CharField(max_length=45)
    write_market = models.ForeignKey(Market, models.DO_NOTHING, db_column='write_market')
    writer_uuid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='writer_uuid')
    hope_price = models.IntegerField()
    bargain_price = models.IntegerField()
    start_date = models.BigIntegerField()
    end_date = models.BigIntegerField()
    ingredients = models.CharField(max_length=1000)
    post_date = models.BigIntegerField()
    update_date = models.BigIntegerField()
    contents = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'post'


class Review(models.Model):
    review_uuid = models.CharField(primary_key=True, max_length=36)
    writer_uuid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='writer_uuid')
    market_reg_num = models.ForeignKey(Market, models.DO_NOTHING, db_column='market_reg_num')
    contents = models.CharField(max_length=1000)
    review_date = models.BigIntegerField()
    star = models.IntegerField()
    hashtag = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'review'
