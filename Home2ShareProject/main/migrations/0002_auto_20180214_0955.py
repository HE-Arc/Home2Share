# Generated by Django 2.0.1 on 2018-02-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='slug_name',
            field=models.SlugField(editable=False, unique=True),
        ),
    ]
