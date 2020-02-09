# Generated by Django 3.0.2 on 2020-02-02 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_blog_read_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_count', models.PositiveIntegerField(default=0, verbose_name='阅读量')),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
    ]