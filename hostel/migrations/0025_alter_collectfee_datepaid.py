# Generated by Django 3.2.4 on 2022-09-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0024_auto_20220914_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectfee',
            name='datepaid',
            field=models.DateField(auto_now_add=True),
        ),
    ]
