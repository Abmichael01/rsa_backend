# Generated by Django 4.2.13 on 2024-06-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_hostel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='secret_key',
            field=models.CharField(default='', max_length=20),
        ),
    ]
