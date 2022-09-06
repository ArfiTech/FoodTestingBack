from django.db import models

# Create your models here.


class NewTable(models.Model):
    uuid = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=30)
    name = models.CharField(max_length=15)
    age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'new_table'

    def __str__(self):
        return self.uuid