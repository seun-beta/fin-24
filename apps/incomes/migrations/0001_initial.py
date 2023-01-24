# Generated by Django 4.1.2 on 2022-10-29 17:31

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Income",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField()),
                ("note", models.CharField(blank=True, max_length=512, null=True)),
                ("place_of_payment", models.CharField(max_length=512)),
                (
                    "description",
                    models.CharField(blank=True, max_length=1024, null=True),
                ),
                ("image", models.URLField()),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="IncomeType",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
