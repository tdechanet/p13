# Generated by Django 4.1.6 on 2023-03-17 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_program_created_at_program_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='program',
            name='updated_at',
        ),
    ]