# Generated by Django 4.2.6 on 2023-11-08 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line_user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
