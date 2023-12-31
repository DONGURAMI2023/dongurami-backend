# Generated by Django 4.1.7 on 2023-11-12 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_user_email_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="accounts\\images\\profile"
            ),
        ),
    ]
