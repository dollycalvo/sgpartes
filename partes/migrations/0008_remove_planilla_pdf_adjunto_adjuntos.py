# Generated by Django 4.2.7 on 2024-02-09 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partes', '0007_remove_permisoespecial_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planilla',
            name='pdf_adjunto',
        ),
        migrations.CreateModel(
            name='Adjuntos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_archivo', models.TextField(default='')),
                ('planilla', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='partes.planilla')),
            ],
        ),
    ]
