# Generated by Django 3.0.2 on 2020-02-03 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20200131_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='mobile',
            field=models.CharField(blank=True, db_column='mobile_number', max_length=100, verbose_name='电话号码'),
        ),
    ]
