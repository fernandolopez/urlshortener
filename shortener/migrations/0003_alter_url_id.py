# Generated by Django 5.0.3 on 2024-03-12 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0002_alter_url_slug_url_shortener_u_slug_0cb73a_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
