# Generated by Django 3.1.2 on 2022-01-20 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0041_indtariff_nationalization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indtariff',
            name='nationalization',
            field=models.FloatField(default=1.0),
        ),
    ]
