# Generated by Django 3.1.3 on 2021-03-01 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210228_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]