# Generated by Django 2.1 on 2019-01-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_update_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='login',
            field=models.CharField(default='', max_length=64),
        ),
    ]