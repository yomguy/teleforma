# Generated by Django 3.2.3 on 2022-05-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teleforma', '0015_auto_20211210_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='siret',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='Siret'),
        ),
    ]