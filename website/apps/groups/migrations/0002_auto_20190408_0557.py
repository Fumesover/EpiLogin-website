# Generated by Django 2.1.5 on 2019-04-08 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='login',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='update',
            old_name='login',
            new_name='email',
        ),
        migrations.AlterField(
            model_name='ban',
            name='type',
            field=models.CharField(choices=[('group', 'GROUP'), ('email', 'EMAIL'), ('user', 'USER')], max_length=64),
        ),
        migrations.AlterField(
            model_name='update',
            name='ban_type',
            field=models.CharField(choices=[('group', 'GROUP'), ('email', 'EMAIL'), ('user', 'USER')], max_length=20),
        ),
    ]
