# Generated by Django 4.1.7 on 2023-04-02 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_count_delete_passwordresetcount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Count',
        ),
    ]
