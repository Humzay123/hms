# Generated by Django 3.2.4 on 2022-09-10 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0019_alter_boarder_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boarder',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='students_pics/'),
        ),
    ]
