# Generated by Django 4.2.1 on 2023-07-30 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_alter_order_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={
                "ordering": ["user__first_name", "user__last_name"],
                "permissions": [("view_history", "can view history")],
            },
        ),
    ]
