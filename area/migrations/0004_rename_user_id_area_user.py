# Generated by Django 4.2.7 on 2023-11-11 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_alter_area_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='user_id',
            new_name='user',
        ),
    ]
