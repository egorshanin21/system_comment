# Generated by Django 5.1.2 on 2024-11-08 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_alter_comment_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
    ]
