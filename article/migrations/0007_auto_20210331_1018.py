# Generated by Django 3.1.7 on 2021-03-31 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20210331_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='t_tag',
        ),
    ]
