# Generated by Django 4.1.2 on 2022-11-10 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0066_hexes_ammunition_hexes_food_hexes_gold_hexes_metal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gameEnd',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='App.player'),
        ),
    ]
