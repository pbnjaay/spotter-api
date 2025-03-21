# Generated by Django 5.1.7 on 2025-03-17 13:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='status',
        ),
        migrations.AddField(
            model_name='eldlog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eldlog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='routestop',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='routestop',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
