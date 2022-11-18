from django.db import models

# Create your models here.


class NewTable(models.Model):
    uuid = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30)
    name = models.CharField(max_length=15)
    age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_table'


class Customer(models.Model):
    uuid = models.CharField(primary_key=True, max_length=36)
    password = models.CharField(max_length=15)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=17, blank=True, null=True)
    gender = models.CharField(max_length=1)
    born_date = models.CharField(max_length=10, blank=True, null=True)
    customer_type = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'customer'


class Market(models.Model):
    reg_num = models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=20)
    market_photo = models.CharField(max_length=255)
    start_date = models.BigIntegerField()
    period = models.BigIntegerField()
    customer_uuid = models.ForeignKey(
        Customer, related_name='customer', on_delete=models.CASCADE, db_column='customer_uuid')
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    phone_num = models.CharField(max_length=13)
    category = models.CharField(max_length=10)
    business_hours = models.BigIntegerField()
    congestion_degree = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'market'


class Post(models.Model):
    post_uuid = models.CharField(primary_key=True, max_length=36)
    subject = models.CharField(max_length=45)
    write_market = models.ForeignKey(
        Market, models.DO_NOTHING, db_column='write_market')
    writer_uuid = models.ForeignKey(
        Customer, models.DO_NOTHING, db_column='writer_uuid')
    hope_price = models.IntegerField()
    discounted_price = models.IntegerField()
    start_date = models.BigIntegerField()
    end_date = models.BigIntegerField()
    ingredients = models.CharField(max_length=1000)
    post_date = models.BigIntegerField()
    update_date = models.BigIntegerField()
    contents = models.CharField(max_length=1000)
    menu_photo = models.ImageField(upload_to="img")
    #is_break = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class Quesbymarket(models.Model):
    market_reg_num = models.OneToOneField(
        Market, models.DO_NOTHING, db_column='market_reg_num', primary_key=True)
    ques_uuid = models.ForeignKey(
        'Questionlist', models.DO_NOTHING, db_column='ques_uuid')

    class Meta:
        managed = False
        db_table = 'quesbymarket'
        unique_together = (('market_reg_num', 'ques_uuid'),)


class Questionlist(models.Model):
    ques_uuid = models.CharField(primary_key=True, max_length=36)
    market_reg_num = models.ForeignKey(
        Market, models.DO_NOTHING, db_column='market_reg_num')
    contents = models.CharField(max_length=200)
    fast_response = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionlist'


class Review(models.Model):
    review_uuid = models.CharField(primary_key=True, max_length=36)
    writer_uuid = models.ForeignKey(
        Customer, models.DO_NOTHING, db_column='writer_uuid')
    market_reg_num = models.ForeignKey(
        Market, models.DO_NOTHING, db_column='market_reg_num')
    ques_uuid = models.ForeignKey(
        Questionlist, models.DO_NOTHING, db_column='ques_uuid', blank=True, null=True)
    review_line = models.CharField(max_length=500)
    review_date = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'review'
