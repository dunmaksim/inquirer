# Generated by Django 2.2.10 on 2020-11-27 18:14

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interrogation',
            old_name='active',
            new_name='is_active',
        ),
    ]
