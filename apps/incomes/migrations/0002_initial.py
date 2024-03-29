# Generated by Django 4.1.2 on 2022-10-29 17:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("incomes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="incometype",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="income",
            name="income_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="incomes.incometype"
            ),
        ),
        migrations.AddField(
            model_name="income",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
