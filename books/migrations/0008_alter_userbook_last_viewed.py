# Generated by Django 5.1.3 on 2024-12-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_userbook_last_viewed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbook',
            name='last_viewed',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
