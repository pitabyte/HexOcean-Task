# Generated by Django 4.0.6 on 2022-11-11 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hexCodeTask', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='heights',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='hexCodeTask.tier'),
        ),
    ]
