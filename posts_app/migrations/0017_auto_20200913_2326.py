# Generated by Django 3.0 on 2020-09-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0016_auto_20200913_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, default='this is you status', max_length=200, null=True),
        ),
    ]
