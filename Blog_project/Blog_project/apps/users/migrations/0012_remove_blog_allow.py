# Generated by Django 2.1.8 on 2020-03-26 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_blog_register_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='allow',
        ),
    ]
