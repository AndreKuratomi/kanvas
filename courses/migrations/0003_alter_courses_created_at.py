# Generated by Django 4.0.3 on 2022-03-17 20:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_courses_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]