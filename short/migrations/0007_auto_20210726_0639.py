# Generated by Django 3.2.4 on 2021-07-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('short', '0006_auto_20210725_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsurl',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='statsurl',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]