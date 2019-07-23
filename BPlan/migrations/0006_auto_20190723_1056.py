# Generated by Django 2.1.3 on 2019-07-23 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BPlan', '0005_auto_20190714_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryoperation',
            name='inventory_operation_user_browser',
            field=models.CharField(default='未知的浏览器', max_length=30, verbose_name='浏览器'),
        ),
        migrations.AddField(
            model_name='inventoryoperation',
            name='inventory_operation_user_device',
            field=models.CharField(default='未知的设备', max_length=30, verbose_name='设备'),
        ),
        migrations.AddField(
            model_name='inventoryoperation',
            name='inventory_operation_user_system',
            field=models.CharField(default='未知的系统', max_length=30, verbose_name='操作系统'),
        ),
    ]