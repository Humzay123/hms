# Generated by Django 3.2.4 on 2022-07-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feetype',
            name='duedate',
            field=models.DateField(verbose_name='due date'),
        ),
    ]
