# Generated by Django 4.1.9 on 2023-08-31 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0031_alter_peticion_estadovalidacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='SIP',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
