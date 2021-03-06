# Generated by Django 2.0.2 on 2018-03-12 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20180303_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.House')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(max_length=255, verbose_name='Message'),
        ),
        migrations.AddField(
            model_name='house',
            name='evaluations',
            field=models.ManyToManyField(through='main.Evaluation', to=settings.AUTH_USER_MODEL),
        ),
    ]
