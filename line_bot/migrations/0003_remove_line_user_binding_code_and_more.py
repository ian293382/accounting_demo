# Generated by Django 4.2.6 on 2023-11-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0002_alter_line_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='line_user',
            name='binding_code',
        ),
        migrations.RemoveField(
            model_name='line_user',
            name='is_bound',
        ),
        migrations.AddField(
            model_name='line_user',
            name='line_user_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
