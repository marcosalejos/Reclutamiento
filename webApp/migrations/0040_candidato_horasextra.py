# Generated by Django 4.1.9 on 2023-12-05 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0039_alter_candidato_tallachaqueta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='HorasExtra',
            field=models.CharField(choices=[('Tecnico 1', 'Tecnico 1'), ('Tecnico 2', 'Tecnico 2'), ('Tecnico 3', 'Tecnico 3'), ('Jefe Equipo', 'Jefe Equipo'), ('Tecnico Junior', 'Tecnico Junior'), ('Tecnico Semi Senior', 'Tecnico Semi Senior'), ('Tecnico Master', 'Tecnico Master')], default='Tecnico 1', max_length=40, null=True),
        ),
    ]
