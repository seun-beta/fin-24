# Generated by Django 4.1.2 on 2022-10-31 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_userpin_userotp_userpin_pin_index_userotp_otp_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="auth_provider",
            field=models.CharField(
                choices=[
                    ("email", "email"),
                    ("google", "google"),
                    ("facebook", "facebook"),
                ],
                default="email",
                max_length=8,
            ),
        ),
    ]
