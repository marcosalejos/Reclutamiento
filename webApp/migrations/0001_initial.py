# Generated by Django 4.1.9 on 2023-05-19 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Peticion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Solicitante', models.CharField(max_length=200)),
                ('Puesto', models.CharField(max_length=200)),
                ('Centro', models.CharField(max_length=100)),
                ('Motivo', models.TextField(null=True)),
                ('Vacantes', models.IntegerField(null=True)),
                ('Observaciones', models.TextField(null=True)),
                ('OfertaID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.oferta')),
            ],
        ),
        migrations.CreateModel(
            name='EntradaOferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Inscritos', models.IntegerField()),
                ('EnProceso', models.IntegerField()),
                ('Finalistas', models.IntegerField()),
                ('Contratados', models.IntegerField()),
                ('Descartados', models.IntegerField()),
                ('fechaPublicacion', models.DateField()),
                ('fechaActual', models.DateField()),
                ('Estado', models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo', max_length=8)),
                ('InscTot', models.IntegerField()),
                ('OfertaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webApp.oferta')),
            ],
        ),
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('DNI', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=100)),
                ('FechaNacimiento', models.DateField()),
                ('Sexo', models.CharField(max_length=20)),
                ('Nacionalidad', models.CharField(max_length=50)),
                ('Telefono', models.IntegerField()),
                ('Mail', models.CharField(max_length=150, null=True)),
                ('ImgDNI', models.CharField(max_length=500, null=True)),
                ('ImgSIP', models.CharField(max_length=500, null=True)),
                ('Municipio', models.CharField(max_length=100, null=True)),
                ('CP', models.IntegerField(null=True)),
                ('Provincia', models.CharField(max_length=75, null=True)),
                ('EntidadBancaria', models.CharField(max_length=200, null=True)),
                ('IBAN', models.CharField(max_length=24, null=True)),
                ('Domicilio', models.CharField(max_length=300, null=True)),
                ('OfertaID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.oferta')),
                ('PeticionID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webApp.peticion')),
            ],
        ),
    ]
