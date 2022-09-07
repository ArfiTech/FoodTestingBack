from django.db import models

# Create your models here.


class NewTable(models.Model):
    uuid = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'new_table'

    def __str__(self):
        return self.uuid