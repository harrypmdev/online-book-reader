# Generated by Django 5.1.3 on 2024-12-10 18:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_userbook_progress"),
    ]

    operations = [
        migrations.AddField(
            model_name="userbook",
            name="color",
            field=models.CharField(default="primary", max_length=20),
        ),
    ]
