# Generated by Django 3.2.8 on 2021-10-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TheEyeApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='app_secret',
            field=models.CharField(default='BquaDdKMtrkzeJPHnchUFbGxRCiNpT', max_length=30),
        ),
    ]
