# Generated by Django 3.2.9 on 2021-11-15 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoApp', '0002_alter_contract_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupclient',
            name='client_id',
        ),
        migrations.AddField(
            model_name='groupclient',
            name='client',
            field=models.ManyToManyField(blank=True, null=True, to='djangoApp.Client'),
        ),
    ]
