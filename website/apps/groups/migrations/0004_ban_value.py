# Generated by Django 2.1.3 on 2019-01-28 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_ban'),
    ]

    operations = [
        migrations.AddField(
            model_name='ban',
            name='value',
            field=models.CharField(default='', max_length=64),
        ),
    ]
