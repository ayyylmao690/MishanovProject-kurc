# Generated by Django 3.2.9 on 2021-11-18 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoApp', '0006_client_pass_and_serial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='client',
            unique_together=set(),
        ),
    ]
