# Generated by Django 3.0.2 on 2020-01-23 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]