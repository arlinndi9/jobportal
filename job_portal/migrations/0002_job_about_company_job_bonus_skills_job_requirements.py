# Generated by Django 4.2.1 on 2023-05-31 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='about_company',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='bonus_skills',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='requirements',
            field=models.TextField(null=True),
        ),
    ]
