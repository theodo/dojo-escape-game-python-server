# Generated by Django 2.2.5 on 2019-10-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0005_user_hint")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="hint_color",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="hint_location",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="explicit_password",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
