# Generated by Django 4.2.13 on 2024-06-17 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
    ]
