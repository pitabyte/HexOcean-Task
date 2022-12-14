# Generated by Django 4.0.6 on 2022-11-14 13:14

from django.db import migrations, models
import hexCodeTask.models


class Migration(migrations.Migration):

    dependencies = [
        ('hexCodeTask', '0007_binaryphoto_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='binaryphoto',
            name='path',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hexCodeTask.models.user_directory_path),
        ),
    ]
