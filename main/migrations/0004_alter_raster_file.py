# Generated by Django 4.1.5 on 2023-01-06 18:29

from django.db import migrations, models
import functools
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_users_raster_user_rename_users_vector_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raster',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(main.models.upload_to, *(), **{'path': 'raster'}), validators=[main.models.validate_file_extension_raster]),
        ),
    ]
