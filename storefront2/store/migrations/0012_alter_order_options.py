# Generated by Django 4.2.1 on 2023-07-28 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0011_alter_customer_options_remove_customer_email_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"permissions": [("cancel_order", "Can cancel order")]},
        ),
    ]