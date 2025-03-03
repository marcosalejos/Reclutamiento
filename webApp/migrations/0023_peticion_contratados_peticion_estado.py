# Generated by Django 4.1.9 on 2023-07-25 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0022_alter_observacion_oferta'),
    ]

    operations = [
        migrations.AddField(
            model_name='peticion',
            name='Contratados',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='peticion',
            name='Estado',
            field=models.CharField(choices=[('Nueva', 'Nueva'), ('Validada', 'Validada'), ('Finalizada', 'Finalizada')], default='Nueva', max_length=10),
        ),
    ]
