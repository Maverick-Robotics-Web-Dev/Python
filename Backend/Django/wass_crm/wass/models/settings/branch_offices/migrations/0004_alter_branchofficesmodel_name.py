# Generated by Django 5.1.2 on 2024-11-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_offices', '0003_alter_branchofficesmodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchofficesmodel',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Nombre'),
        ),
    ]
