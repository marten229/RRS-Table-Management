# Generated by Django 5.0.4 on 2024-05-26 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TableManagement', '0007_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='restaurant',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
        migrations.DeleteModel(
            name='Table',
        ),
    ]
