# Generated by Django 3.2.13 on 2022-06-27 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="forumuser",
            name="birthdate",
        ),
    ]
