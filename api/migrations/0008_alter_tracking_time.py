# Generated by Django 3.2.12 on 2022-06-22 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_tracking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
