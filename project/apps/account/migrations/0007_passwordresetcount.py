# Generated by Django 4.1.7 on 2023-04-03 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_delete_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
