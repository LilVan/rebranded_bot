# Generated by Django 4.1.7 on 2023-04-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj_maths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='doctor_user_name',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
