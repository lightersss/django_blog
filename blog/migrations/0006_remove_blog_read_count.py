# Generated by Django 3.0.2 on 2020-02-02 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blog_read_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='read_count',
        ),
    ]
