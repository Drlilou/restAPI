# Generated by Django 3.2.12 on 2022-08-30 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_user_firebaseid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='typeclient',
            field=models.CharField(default='simple', max_length=200),
        ),
    ]