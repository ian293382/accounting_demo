# Generated by Django 4.2.6 on 2023-11-03 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial_records', '0004_alter_financialrecord_currency'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='financialrecord',
            options={'ordering': ('-created_at',)},
        ),
    ]
