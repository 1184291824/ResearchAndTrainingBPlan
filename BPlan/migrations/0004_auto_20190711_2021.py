# Generated by Django 2.1.3 on 2019-07-11 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BPlan', '0003_auto_20190628_1633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginrecord',
            options={'ordering': ['-login_time'], 'verbose_name_plural': '访问记录'},
        ),
        migrations.RemoveField(
            model_name='loginrecord',
            name='login_location',
        ),
    ]