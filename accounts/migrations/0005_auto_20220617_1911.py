# Generated by Django 3.2.5 on 2022-06-17 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220617_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=50, null=True),
        ),
    ]
