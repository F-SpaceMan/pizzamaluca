# Generated by Django 4.2.2 on 2023-07-08 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='identifier',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
