# Generated by Django 4.1 on 2022-09-24 16:57

from django.db import migrations, models
import django.db.models.deletion


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
                ("gender", models.CharField(max_length=1)),
                ("born_date", models.CharField(blank=True, max_length=10, null=True)),
                ("customer_type", models.CharField(max_length=1)),
            ],
            options={"db_table": "customer", "managed": False,},
        ),
        migrations.CreateModel(
            name="Market",
            fields=[
                (
                    "reg_num",
                    models.CharField(max_length=12, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=20)),
                ("market_photo", models.CharField(max_length=255)),
                ("start_date", models.BigIntegerField()),
                ("period", models.BigIntegerField()),
                ("location", models.CharField(max_length=200)),
                ("latitude", models.FloatField()),
                ("longtitude", models.FloatField()),
                ("phone_num", models.CharField(max_length=13)),
                ("category", models.CharField(max_length=10)),
                ("business_hours", models.BigIntegerField()),
                (
                    "congestion_degree",
                    models.CharField(blank=True, max_length=45, null=True),
                ),
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
                ("discounted_price", models.IntegerField()),
                ("start_date", models.BigIntegerField()),
                ("end_date", models.BigIntegerField()),
                ("ingredients", models.CharField(max_length=1000)),
                ("post_date", models.BigIntegerField()),
                ("update_date", models.BigIntegerField()),
                ("contents", models.CharField(max_length=1000)),
                ("menu_photo", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={"db_table": "post", "managed": False,},
        ),
        migrations.CreateModel(
            name="Questionlist",
            fields=[
                (
                    "ques_uuid",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("contents", models.CharField(max_length=200)),
                (
                    "fast_response",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
            ],
            options={"db_table": "questionlist", "managed": False,},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "review_uuid",
                    models.CharField(max_length=36, primary_key=True, serialize=False),
                ),
                ("review_line", models.CharField(max_length=500)),
                ("review_date", models.BigIntegerField()),
            ],
            options={"db_table": "review", "managed": False,},
        ),
        migrations.CreateModel(
            name="Quesbymarket",
            fields=[
                (
                    "market_reg_num",
                    models.OneToOneField(
                        db_column="market_reg_num",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="app.market",
                    ),
                ),
            ],
            options={"db_table": "quesbymarket", "managed": False,},
        ),
    ]
