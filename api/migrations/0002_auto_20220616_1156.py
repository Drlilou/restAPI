# Generated by Django 3.2.12 on 2022-06-16 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amite',
            name='id_client',
            field=models.ForeignKey(db_column='id_client', on_delete=django.db.models.deletion.DO_NOTHING, to='api.client'),
        ),
        migrations.AlterField(
            model_name='amite',
            name='id_driver',
            field=models.ForeignKey(db_column='id_driver', on_delete=django.db.models.deletion.DO_NOTHING, to='api.driver'),
        ),
    ]