# Generated by Django 2.1.3 on 2019-07-25 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPlan', '0008_inventoryoperation_inventory_operation_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginrecord',
            name='login_location',
            field=models.CharField(default='未知位置', max_length=30, verbose_name='位置'),
        ),
    ]
