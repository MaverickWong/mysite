# Generated by Django 2.1.2 on 2019-07-26 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20190726_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugitem',
            name='min_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='drugitem',
            name='status',
            field=models.PositiveIntegerField(blank=True, choices=[(0, ''), (1, '充足'), (2, '待补充'), (3, '缺货'), (4, '分类1')], null=True),
        ),
    ]
