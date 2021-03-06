# Generated by Django 2.2.9 on 2020-01-24 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Datapoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energy_expected', models.FloatField(verbose_name='Expected energy')),
                ('energy_observed', models.FloatField(verbose_name='Observed energy')),
                ('irradiation_observed', models.FloatField(verbose_name='Observed irradiation')),
                ('irradiation_expected', models.FloatField(verbose_name='Expected irradiation')),
                ('plant_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Plant')),
            ],
        ),
    ]
