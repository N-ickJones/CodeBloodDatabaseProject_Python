# Generated by Django 2.1.2 on 2018-11-12 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileimage',
            name='username',
            field=models.CharField(default='none', max_length=50),
        ),
    ]