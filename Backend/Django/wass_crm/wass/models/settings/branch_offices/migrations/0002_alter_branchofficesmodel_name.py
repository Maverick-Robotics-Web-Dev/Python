# Generated by Django 5.1.2 on 2024-11-06 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_offices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchofficesmodel',
            name='name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Nombre'),
        ),
    ]
