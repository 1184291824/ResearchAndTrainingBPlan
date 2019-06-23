# Generated by Django 2.2.2 on 2019-06-23 09:19

from django.db import migrations, models
import django.db.models.deletion


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
                ('user_password', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=12)),
                ('user_gender', models.BooleanField(default=True)),
                ('user_identity', models.CharField(default='1', max_length=20)),
                ('user_question', models.CharField(blank=True, default='', max_length=20)),
                ('user_question_answer', models.CharField(blank=True, default='', max_length=20)),
                ('user_create_time', models.DateTimeField(auto_now_add=True)),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BPlan.Group')),
            ],
            options={
                'db_table': 'User',
                'ordering': ['id'],
            },
        ),
    ]
