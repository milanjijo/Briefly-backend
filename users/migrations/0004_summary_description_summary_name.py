# Generated by Django 4.2 on 2023-05-15 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_email_summary_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
