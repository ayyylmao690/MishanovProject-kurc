# Generated by Django 3.2.8 on 2021-10-26 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('patronymic', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('pass_number', models.CharField(max_length=6)),
                ('pass_serial', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('money', models.CharField(max_length=30)),
                ('language', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('patronymic', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('access', models.CharField(choices=[('1', '1'), ('0', '0')], default=0, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='VisaType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Visa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visa_number', models.CharField(max_length=10)),
                ('visa_serial', models.CharField(max_length=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.client')),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.country')),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.visatype')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('town', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('wi_fi', models.CharField(choices=[('1', '1'), ('0', '0')], default=0, max_length=30)),
                ('beach', models.CharField(choices=[('1', '1'), ('0', '0')], default=0, max_length=30)),
                ('air_conditioning', models.CharField(choices=[('1', '1'), ('0', '0')], default=0, max_length=30)),
                ('child', models.CharField(choices=[('1', '1'), ('0', '0')], default=0, max_length=30)),
                ('bar', models.CharField(choices=[('1', '1'), ('0', '0')], default=0, max_length=30)),
                ('desc', models.TextField(max_length=200)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.country')),
            ],
        ),
        migrations.CreateModel(
            name='GroupClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.client')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('contact_number', models.CharField(max_length=10)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.client')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.groupclient')),
                ('hotel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoApp.hotel')),
            ],
        ),
    ]
