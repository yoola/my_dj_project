# Generated by Django 2.1 on 2018-10-27 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoogleGlass', '0010_auto_20181017_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='object_id',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='document',
            name='todo',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]