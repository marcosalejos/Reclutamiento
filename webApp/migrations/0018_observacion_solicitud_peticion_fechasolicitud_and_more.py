# Generated by Django 4.1.9 on 2023-06-24 22:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0017_remove_registro_procesadamail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='observacion',
            name='Solicitud',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='webApp.peticion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peticion',
            name='FechaSolicitud',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='peticion',
            name='Motivo',
            field=models.TextField(default=11),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='peticion',
            name='Vacantes',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]