# Generated by Django 4.1.9 on 2023-08-18 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0028_candidato_centrocomp'),
    ]

    operations = [
        migrations.AddField(
            model_name='peticion',
            name='EstadoValidacion',
            field=models.CharField(choices=[('Aprovada', 'Aprovada'), ('Denegada', 'Denegada')], max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='peticion',
            name='MotivoDenegado',
            field=models.TextField(null=True),
        ),
    ]
