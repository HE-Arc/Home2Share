# Generated by Django 2.0.2 on 2018-04-06 17:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20180316_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='comments',
            field=models.ManyToManyField(related_name='comments_houses', through='main.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='house',
            name='evaluations',
            field=models.ManyToManyField(related_name='evaluations_houses', through='main.Evaluation', to=settings.AUTH_USER_MODEL),
        ),
    ]