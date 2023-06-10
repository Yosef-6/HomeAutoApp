# Generated by Django 4.2.2 on 2023-06-06 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('hardwareID', models.BigIntegerField(primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceName', models.CharField(max_length=200)),
                ('pinNumber', models.PositiveSmallIntegerField()),
                ('modeOperation', models.BooleanField()),
                ('useStateVal', models.BooleanField()),
                ('state', models.BooleanField()),
                ('floatValue', models.FloatField()),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Entries', to='homeApp.hardware')),
            ],
        ),
    ]