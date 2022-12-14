# Generated by Django 4.0.6 on 2022-11-12 19:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hexCodeTask', '0005_thumbnail_url_tier_gets_original_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tier',
            name='expiring_link',
            field=models.BooleanField(null=True),
        ),
        migrations.CreateModel(
            name='BinaryPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=20, null=True)),
                ('expires', models.IntegerField(validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(30000)])),
                ('photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='binary', to='hexCodeTask.photo')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='binary', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
