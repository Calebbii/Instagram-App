# Generated by Django 3.2.9 on 2021-12-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_alter_image_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_name',
            field=models.CharField(max_length=200),
        ),
    ]
