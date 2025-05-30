# Generated by Django 5.2 on 2025-05-18 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0003_rename_created_by_department_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='entryexitlog',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='externalperson',
            name='register_user',
        ),
        migrations.RemoveField(
            model_name='toolcategory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='tools',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='tooltransferlog',
            name='registering_user',
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entryexitlog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='externalperson',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='toolcategory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='toolCategory'),
        ),
        migrations.AddField(
            model_name='tools',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tooltransferlog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='externalperson',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='worklog.peoplecategory'),
        ),
    ]
