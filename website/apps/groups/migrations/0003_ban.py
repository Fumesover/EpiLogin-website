# Generated by Django 2.1.3 on 2019-01-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20190127_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('S', 'SERVER'), ('L', 'LOGIN'), ('U', 'USER')], max_length=64)),
            ],
        ),
    ]
