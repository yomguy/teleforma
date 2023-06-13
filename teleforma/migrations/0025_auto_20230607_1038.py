# Generated by Django 3.2.13 on 2023-06-07 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teleforma', '0024_auto_20230316_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='corrections_shared',
            field=models.BooleanField(default=False, help_text='A utiliser avec le champ relatif dans la période.', verbose_name='Corrections partagés'),
        ),
        migrations.AddField(
            model_name='period',
            name='corrections_from',
            field=models.ForeignKey(blank=True, help_text="Permet d'afficher les séminaires de corrections d'une autre période. Il faut aussi cocher la case relative dans les matières pour autoriser celles-ci à partager leur contenu.", null=True, on_delete=django.db.models.deletion.SET_NULL, to='teleforma.period', verbose_name='Récupérer les séminaires de correction depuis'),
        ),
    ]
