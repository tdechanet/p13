# Generated by Django 4.1.6 on 2023-03-22 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_program_id_favorite_try_program_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='try_program',
            new_name='program_id',
        ),
        migrations.RenameField(
            model_name='favorite',
            old_name='try_user',
            new_name='user_id',
        ),
    ]