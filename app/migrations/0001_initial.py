# Generated by Django 4.1 on 2022-09-14 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "uuid",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("password", models.CharField(max_length=15)),
                ("email", models.CharField(max_length=64)),
                ("name", models.CharField(blank=True, max_length=17, null=True)),
                ("nickname", models.CharField(blank=True, max_length=45, null=True)),
                ("gender", models.CharField(max_length=1)),
                ("profile_photo", models.TextField(blank=True, null=True)),
                ("born_date", models.CharField(blank=True, max_length=10, null=True)),
                ("customer_type", models.CharField(max_length=1)),
            ],
            options={"db_table": "customer", "managed": False,},
        ),
        migrations.CreateModel(
            name="Market",
            fields=[
                ("reg_num", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=20)),
                ("menu_photo", models.TextField()),
                ("start_date", models.BigIntegerField()),
                ("location", models.CharField(max_length=200)),
                ("latitude", models.FloatField()),
                ("longtitude", models.FloatField()),
                ("phone_num", models.CharField(max_length=13)),
                ("category", models.CharField(max_length=10)),
                ("hashtag", models.CharField(max_length=1000)),
            ],
            options={"db_table": "market", "managed": False,},
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "post_uuid",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("subject", models.CharField(max_length=45)),
                ("hope_price", models.IntegerField()),
                ("bargain_price", models.IntegerField()),
                ("start_date", models.BigIntegerField()),
                ("end_date", models.BigIntegerField()),
                ("ingredients", models.CharField(max_length=1000)),
                ("post_date", models.BigIntegerField()),
                ("update_date", models.BigIntegerField()),
                ("contents", models.CharField(max_length=1000)),
            ],
            options={"db_table": "post", "managed": False,},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "review_uuid",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("contents", models.CharField(max_length=1000)),
                ("review_date", models.BigIntegerField()),
                ("star", models.IntegerField()),
                ("hashtag", models.CharField(max_length=1000)),
            ],
            options={"db_table": "review", "managed": False,},
        ),
    ]
