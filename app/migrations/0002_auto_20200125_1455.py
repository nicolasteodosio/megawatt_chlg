# Generated by Django 2.2.9 on 2020-01-25 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Energy', 'energy'), ('Irradiation', 'irradiation')], max_length=15, verbose_name='Type of report')),
                ('expected', models.FloatField(verbose_name='Expected')),
                ('observed', models.FloatField(verbose_name='Observed')),
                ('plant_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Plant')),
            ],
        ),
        migrations.DeleteModel(
            name='Datapoint',
        ),
    ]