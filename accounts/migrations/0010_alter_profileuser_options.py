# Generated by Django 5.2 on 2025-05-06 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profileuser',
            options={'ordering': ('-created_at',), 'verbose_name': 'ProfileUser', 'verbose_name_plural': 'ProfileUser'},
        ),
    ]
