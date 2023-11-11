# Generated by Django 4.2.7 on 2023-11-11 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_alter_area_user_id'),
        ('accounts', '0006_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointHistory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gain', models.IntegerField()),
                ('total', models.IntegerField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area.area')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]