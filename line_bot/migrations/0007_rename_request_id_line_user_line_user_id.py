# Generated by Django 4.2.6 on 2023-11-14 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('line_bot', '0006_rename_line_user_id_line_user_request_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line_user',
            old_name='request_id',
            new_name='line_user_id',
        ),
    ]
