# Generated by Django 2.0.5 on 2018-05-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0011_auto_20180530_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyrecord',
            name='user',
            field=models.CharField(default='root', help_text='事件记录人', max_length=30),
        ),
    ]