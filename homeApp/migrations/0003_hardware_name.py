# Generated by Django 4.2.2 on 2023-06-07 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeApp', '0002_remove_device_usestateval_device_usage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardware',
            name='name',
            field=models.CharField(default='not specified', max_length=100),
        ),
    ]
