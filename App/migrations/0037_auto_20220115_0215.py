# Generated by Django 3.1.2 on 2022-01-15 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0036_auto_20211206_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='indtariff',
            name='militarySend',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='indtariff',
            name='moneySend',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='investment_restriction',
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('exportRestriction', models.FloatField(default=0)),
                ('subsidy', models.FloatField(default=0)),
                ('controller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.playerproduct')),
            ],
        ),
        migrations.AddField(
            model_name='playerproduct',
            name='curr_player',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='App.player'),
        ),
        migrations.AddField(
            model_name='playerproduct',
            name='game',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='App.game'),
        ),
    ]
