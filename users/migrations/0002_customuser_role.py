# Generated by Django 5.0.4 on 2024-04-18 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.TextField(default='common'),
        ),
    ]