# Generated by Django 2.2.7 on 2020-01-26 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20200125_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/posts/'),
        ),
    ]
