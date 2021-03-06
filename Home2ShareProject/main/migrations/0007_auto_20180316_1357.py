# Generated by Django 2.0.2 on 2018-03-16 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_auto_20180312_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='comments',
            field=models.ManyToManyField(related_name='comments', through='main.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.House'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='house',
            name='evaluations',
            field=models.ManyToManyField(related_name='evaluations', through='main.Evaluation', to=settings.AUTH_USER_MODEL),
        ),
    ]
