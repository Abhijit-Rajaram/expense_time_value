# Generated by Django 5.1.7 on 2025-03-31 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthwise',
            name='month',
            field=models.DateField(),
        ),
    ]
