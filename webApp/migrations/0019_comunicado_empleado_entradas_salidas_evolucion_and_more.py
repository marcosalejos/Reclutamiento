# Generated by Django 4.1.9 on 2023-06-29 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0018_observacion_solicitud_peticion_fechasolicitud_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=50)),
                ('Fecha', models.DateField()),
                ('Tipo', models.CharField(choices=[('Fisico', 'Fisico'), ('Digital', 'Digital'), ('TeamBuildings', 'TeamBuildings')], default='Fisico', max_length=20)),
                ('Tema', models.CharField(max_length=50)),
                ('Eje', models.CharField(max_length=50)),
                ('Impacto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Centro', models.CharField(max_length=75)),
                ('Domicilio', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Entradas_Salidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DNI', models.CharField(max_length=9, null=True)),
                ('FechaBienvenida', models.DateField()),
                ('FechaContratoIni', models.DateField()),
                ('FechaContratoFin', models.DateField()),
                ('Centro', models.CharField(max_length=75)),
                ('TipoMotivo', models.CharField(choices=[('Baja Voluntaria', 'Baja Voluntaria'), ('Despido', 'Despido')], default='Baja Voluntaria', max_length=20)),
                ('Motivo', models.CharField(choices=[('Desplazamiento a ct', 'Desplazamiento a ct'), ('Turnistica', 'Turnistica'), ('Retribucion', 'Retribucion'), ('Oferta de otra empresa', 'Oferta otra empresa'), ('Proyecto personal/familiar', 'Proyecto personal/familiar'), ('Otros', 'Otros')], default='Desplazamiento a ct', max_length=50)),
                ('TipoSalidaForzada', models.CharField(max_length=1)),
                ('Grupo', models.CharField(max_length=50)),
                ('Convenio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Evolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Participantes', models.IntegerField()),
                ('Trabajadores', models.IntegerField()),
                ('Centro', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DNI', models.CharField(max_length=9)),
                ('Nombre', models.CharField(max_length=50)),
                ('FechaEvolucion', models.DateField()),
                ('FechaAplicacion', models.DateField()),
                ('PuestoOrigen', models.CharField(max_length=75)),
                ('PuestoDest', models.CharField(max_length=75)),
                ('SBA_origen', models.IntegerField()),
                ('SBA_dest', models.IntegerField()),
                ('Coste', models.IntegerField()),
                ('Tipo', models.CharField(choices=[('Entrevista Evolucion', 'Entrevista Evolucion'), ('Contraoferta', 'Contraoferta'), ('Metodo Retencion', 'Metodo Retencion')], default='Entrevista Evolucion', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='candidato',
            name='EmpresaOrigen',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='candidato',
            name='FechaIncorporacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='candidato',
            name='FechaIncorporacionEstimada',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='candidato',
            name='Puesto',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='candidato',
            name='PuestoOrigen',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='oferta',
            name='Interno',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Paso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cantidad', models.IntegerField()),
                ('Tipo', models.CharField(choices=[('Contacto Telefonico', 'Contacto Telefonico'), ('Entrevista de RRHH', 'Entrevista de RRHH'), ('Entrevista Tecnica', 'Entrevista Tecnica'), ('Prueba Tecnica', 'Prueba Tecnica'), ('Oferta', 'Oferta')], default='Contacto Telefonico', max_length=30)),
                ('Apto', models.IntegerField(null=True)),
                ('NoApto', models.IntegerField(null=True)),
                ('Citado', models.IntegerField(null=True)),
                ('Dudoso', models.IntegerField(null=True)),
                ('NoInteresado', models.IntegerField(null=True)),
                ('NoContesta', models.IntegerField(null=True)),
                ('Criba', models.IntegerField(null=True)),
                ('Oferta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webApp.oferta')),
                ('Solicitud', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webApp.peticion')),
            ],
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DNI', models.CharField(max_length=9, null=True)),
                ('Tipo', models.CharField(choices=[('Desplazamiento de residencia a CT', 'Desplazamiento de residencia a CT'), ('Turnistica', 'Turnistica'), ('Retribucion', 'Retribucion'), ('Aceptar otra oferta de incorporacion', 'Aceptar otra oferta de incorporacion'), ('Contraoferta empresa actual', 'Contraoferta empresa actual'), ('Otros', 'Otros')], default='Desplazamiento de residencia a CT', max_length=50)),
                ('Oferta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webApp.oferta')),
            ],
        ),
        migrations.CreateModel(
            name='Externo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DNI', models.CharField(max_length=9, null=True)),
                ('FuenteOrigen', models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Contacto Interno', 'Contacto Interno'), ('Web Corporativa', 'Web Corporativa'), ('Proveedor Externo', 'Proveedor Externo')], default='LinkedIn', max_length=20)),
                ('Oferta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webApp.oferta')),
                ('Solicitud', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webApp.peticion')),
            ],
        ),
    ]
