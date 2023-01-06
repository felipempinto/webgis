# Generated by Django 4.1.5 on 2023-01-06 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_alter_raster_file_remove_raster_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raster',
            name='downloaded',
        ),
        migrations.RemoveField(
            model_name='vector',
            name='downloaded',
        ),
        migrations.AddField(
            model_name='dataset',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner_dataset', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
