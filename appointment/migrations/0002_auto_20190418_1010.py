# Generated by Django 2.1.2 on 2019-04-18 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apptitem',
            name='startDate',
        ),
        migrations.AlterField(
            model_name='dateforappoint',
            name='date',
            field=models.DateField(null=True),
        ),
    ]