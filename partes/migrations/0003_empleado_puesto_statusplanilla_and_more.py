# Generated by Django 4.2.7 on 2023-12-04 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partes', '0002_regeneracionpw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legajo', models.IntegerField()),
                ('apellidos', models.TextField()),
                ('nombres', models.TextField()),
                ('email', models.TextField()),
                ('password', models.CharField(max_length=100)),
                ('jefe_directo', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='partes.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StatusPlanilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='planilla',
            name='agente',
        ),
        migrations.RemoveField(
            model_name='planilla',
            name='presentado',
        ),
        migrations.RemoveField(
            model_name='regeneracionpw',
            name='agente',
        ),
        migrations.AddField(
            model_name='planilla',
            name='pdf_adjunto',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Agentes',
        ),
        migrations.AddField(
            model_name='empleado',
            name='puesto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='partes.puesto'),
        ),
        migrations.AddField(
            model_name='planilla',
            name='empleado',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='partes.empleado'),
        ),
        migrations.AddField(
            model_name='planilla',
            name='status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='partes.statusplanilla'),
        ),
        migrations.AddField(
            model_name='regeneracionpw',
            name='empleado',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='partes.empleado'),
        ),
    ]