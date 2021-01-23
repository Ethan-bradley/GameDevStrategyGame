# Generated by Django 3.1.2 on 2020-12-25 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_economic_game_hexes_player_tariff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='players',
        ),
        migrations.AddField(
            model_name='tariff',
            name='curr_player',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='App.player'),
        ),
        migrations.CreateModel(
            name='IndTariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tariffAm', models.DecimalField(decimal_places=50, max_digits=70)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.tariff')),
                ('key', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.player')),
            ],
        ),
    ]