# Generated by Django 2.1.2 on 2019-04-18 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_auto_20190418_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apptitem',
            name='createDateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apptitem',
            name='endDateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apptitem',
            name='startDateTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]