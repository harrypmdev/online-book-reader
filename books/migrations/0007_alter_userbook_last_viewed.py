# Generated by Django 5.1.3 on 2024-12-12 17:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0006_userbook_percent_progress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userbook",
            name="last_viewed",
            field=models.DateField(auto_now_add=True),
        ),
    ]
