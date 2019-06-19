# Generated by Django 2.2.2 on 2019-06-19 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(max_length=12)),
                ('group_name', models.CharField(max_length=12)),
            ],
            options={
                'db_table': 'Group',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=12)),
                ('user_password_encrypted', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=12)),
                ('user_gender', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'User',
                'ordering': ['id'],
            },
        ),
    ]
