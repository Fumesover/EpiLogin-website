# Generated by Django 2.1.5 on 2019-04-13 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20190408_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
