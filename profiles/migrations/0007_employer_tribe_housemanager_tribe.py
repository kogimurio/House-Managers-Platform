# Generated by Django 5.1.2 on 2024-11-07 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_housemanager_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='tribe',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='housemanager',
            name='tribe',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
