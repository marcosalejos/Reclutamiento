# Generated by Django 4.1.9 on 2023-05-31 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0009_suscriptores'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaRegistro', models.DateField()),
                ('Inscritos', models.IntegerField(null=True)),
                ('I_EP', models.IntegerField(null=True)),
                ('EP_F', models.IntegerField(null=True)),
                ('F_C', models.IntegerField(null=True)),
                ('Descartados', models.IntegerField(null=True)),
                ('Observaciones', models.TextField(null=True)),
            ],
        ),
    ]