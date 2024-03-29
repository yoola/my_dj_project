# Generated by Django 2.1 on 2018-10-16 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GoogleGlass', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('object_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('object_type', models.CharField(blank=True, max_length=10)),
                ('floor', models.CharField(blank=True, max_length=10)),
                ('room', models.CharField(blank=True, max_length=10)),
                ('status', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='floor',
        ),
        migrations.RemoveField(
            model_name='document',
            name='object_type',
        ),
        migrations.RemoveField(
            model_name='document',
            name='room',
        ),
        migrations.RemoveField(
            model_name='document',
            name='status',
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.ImageField(default='documents/None/No_images.jpg/', upload_to='documents/'),
        ),
        migrations.AddField(
            model_name='document',
            name='object_id',
            field=models.ForeignKey(default='DEFAULT VALUE', on_delete=django.db.models.deletion.CASCADE, to='GoogleGlass.Object'),
        ),
    ]
