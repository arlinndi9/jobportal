# Generated by Django 4.2.1 on 2023-06-02 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0004_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.CharField(default='', max_length=255),
        ),
    ]
